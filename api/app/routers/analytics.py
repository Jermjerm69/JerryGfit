from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta
from io import BytesIO
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.risk import Risk, RiskStatus, RiskProbability, RiskImpact
from app.models.ai_request import AIRequest
from app.models.project import Project
from app.schemas.analytics import (
    AnalyticsResponse, AnalyticsTotals, BurndownChart, BurndownDataPoint,
    RiskDistribution, VelocityDataPoint
)
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get analytics data including totals and burndown chart."""

    # Calculate totals
    total_tasks = db.query(Task).filter(Task.owner_id == current_user.id).count()
    completed_tasks = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id, Task.status == TaskStatus.DONE)
        .count()
    )

    total_risks = db.query(Risk).filter(Risk.owner_id == current_user.id).count()
    open_risks = (
        db.query(Risk)
        .filter(Risk.owner_id == current_user.id, Risk.status == RiskStatus.OPEN)
        .count()
    )

    ai_requests_count = (
        db.query(AIRequest).filter(AIRequest.user_id == current_user.id).count()
    )

    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Calculate velocity (tasks completed per week in the last 4 weeks)
    four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
    tasks_completed_last_4_weeks = (
        db.query(Task)
        .filter(
            Task.owner_id == current_user.id,
            Task.status == TaskStatus.DONE,
            Task.updated_at >= four_weeks_ago
        )
        .count()
    )
    velocity = tasks_completed_last_4_weeks / 4.0  # tasks per week

    # Calculate average lead time (average days to complete a task)
    completed_tasks_with_dates = (
        db.query(Task)
        .filter(
            Task.owner_id == current_user.id,
            Task.status == TaskStatus.DONE,
            Task.created_at.isnot(None),
            Task.updated_at.isnot(None)
        )
        .all()
    )

    if completed_tasks_with_dates:
        lead_times = [
            (task.updated_at - task.created_at).total_seconds() / 86400  # Convert to days
            for task in completed_tasks_with_dates
        ]
        average_lead_time = sum(lead_times) / len(lead_times)
    else:
        average_lead_time = 0

    # Calculate risk score (weighted average based on probability and impact)
    # Mapping: low=1, medium=2, high=3, critical=4
    probability_weight = {
        'low': 1,
        'medium': 2,
        'high': 3
    }
    impact_weight = {
        'low': 1,
        'medium': 2,
        'high': 3,
        'critical': 4
    }

    risks_with_scores = (
        db.query(Risk)
        .filter(
            Risk.owner_id == current_user.id,
            Risk.status == RiskStatus.OPEN
        )
        .all()
    )

    if risks_with_scores:
        risk_scores = [
            probability_weight.get(risk.probability.value, 2) * impact_weight.get(risk.impact.value, 2)
            for risk in risks_with_scores
        ]
        # Normalize to 0-100 scale (max possible score is 3*4=12)
        average_risk_score = (sum(risk_scores) / len(risk_scores)) / 12 * 100
    else:
        average_risk_score = 0

    totals = AnalyticsTotals(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_risks=total_risks,
        open_risks=open_risks,
        ai_requests_count=ai_requests_count,
        completion_rate=round(completion_rate, 2),
        velocity=round(velocity, 2),
        average_lead_time=round(average_lead_time, 2),
        risk_score=round(average_risk_score, 2),
    )

    # Generate mock burndown chart data (last 14 days)
    burndown_data = []
    today = datetime.utcnow()

    for i in range(14, -1, -1):
        date = today - timedelta(days=i)
        # Mock calculation - in reality, you'd query historical data
        remaining = max(0, total_tasks - int((14 - i) * (completed_tasks / 14)) if total_tasks > 0 else 0)
        completed = total_tasks - remaining

        burndown_data.append(
            BurndownDataPoint(
                date=date,
                remaining_tasks=remaining,
                completed_tasks=completed,
            )
        )

    burndown = BurndownChart(data_points=burndown_data)

    # Calculate risk distribution by severity
    all_risks = db.query(Risk).filter(Risk.owner_id == current_user.id).all()

    risk_dist = RiskDistribution(
        low=sum(1 for r in all_risks if r.impact.value == 'low'),
        medium=sum(1 for r in all_risks if r.impact.value == 'medium'),
        high=sum(1 for r in all_risks if r.impact.value == 'high'),
        critical=sum(1 for r in all_risks if r.impact.value == 'critical'),
    )

    # Calculate weekly velocity data (last 6 weeks)
    velocity_data_points = []
    for week_num in range(6, 0, -1):
        week_start = datetime.utcnow() - timedelta(weeks=week_num)
        week_end = week_start + timedelta(weeks=1)

        tasks_in_week = db.query(Task).filter(
            Task.owner_id == current_user.id,
            Task.status == TaskStatus.DONE,
            Task.updated_at >= week_start,
            Task.updated_at < week_end
        ).count()

        velocity_data_points.append(
            VelocityDataPoint(
                week=f"Week {7-week_num}",
                tasks_completed=tasks_in_week,
                average=round(velocity, 2)
            )
        )

    return AnalyticsResponse(
        totals=totals,
        burndown=burndown,
        risk_distribution=risk_dist,
        velocity_data=velocity_data_points
    )


@router.get("/export/pdf")
def export_analytics_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export analytics as PDF report."""

    # Get analytics data
    analytics = get_analytics(db, current_user)

    # Get additional data
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    risks = db.query(Risk).filter(Risk.owner_id == current_user.id).all()
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceBefore=20,
        spaceAfter=12,
    )

    # Title
    elements.append(Paragraph(f"Analytics Report - {current_user.full_name or current_user.username}", title_style))
    elements.append(Paragraph(f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Summary Metrics
    elements.append(Paragraph("Summary Metrics", heading_style))
    summary_data = [
        ['Metric', 'Value'],
        ['Total Tasks', str(analytics.totals.total_tasks)],
        ['Completed Tasks', str(analytics.totals.completed_tasks)],
        ['Completion Rate', f"{analytics.totals.completion_rate:.1f}%"],
        ['Velocity', f"{analytics.totals.velocity:.1f} tasks/week"],
        ['Average Lead Time', f"{analytics.totals.average_lead_time:.1f} days"],
        ['Total Risks', str(analytics.totals.total_risks)],
        ['Open Risks', str(analytics.totals.open_risks)],
        ['Risk Score', f"{analytics.totals.risk_score:.1f}/100"],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))

    # Risk Distribution
    elements.append(Paragraph("Risk Distribution", heading_style))
    risk_data = [
        ['Severity', 'Count'],
        ['Low', str(analytics.risk_distribution.low)],
        ['Medium', str(analytics.risk_distribution.medium)],
        ['High', str(analytics.risk_distribution.high)],
        ['Critical', str(analytics.risk_distribution.critical)],
    ]

    risk_table = Table(risk_data, colWidths=[3*inch, 2*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 0.3*inch))

    # Projects
    elements.append(Paragraph(f"Projects ({len(projects)} total)", heading_style))
    if projects:
        project_data = [['Name', 'Status', 'Progress']]
        for project in projects[:10]:  # Limit to 10
            project_data.append([
                project.name,
                project.status.value.upper(),
                f"{project.progress:.0f}%"
            ])

        project_table = Table(project_data, colWidths=[3*inch, 1.5*inch, 1*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(project_table)
    else:
        elements.append(Paragraph("No projects found.", styles['Normal']))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=analytics_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"}
    )


@router.get("/export/excel")
def export_analytics_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export analytics as Excel spreadsheet."""

    # Get data
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    risks = db.query(Risk).filter(Risk.owner_id == current_user.id).all()
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    analytics = get_analytics(db, current_user)

    # Create Excel file
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Metric': ['Total Tasks', 'Completed Tasks', 'Completion Rate', 'Velocity',
                      'Average Lead Time', 'Total Risks', 'Open Risks', 'Risk Score'],
            'Value': [
                analytics.totals.total_tasks,
                analytics.totals.completed_tasks,
                f"{analytics.totals.completion_rate:.1f}%",
                f"{analytics.totals.velocity:.1f} tasks/week",
                f"{analytics.totals.average_lead_time:.1f} days",
                analytics.totals.total_risks,
                analytics.totals.open_risks,
                f"{analytics.totals.risk_score:.1f}/100"
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

        # Tasks sheet
        if tasks:
            tasks_data = {
                'ID': [t.id for t in tasks],
                'Title': [t.title for t in tasks],
                'Status': [t.status.value for t in tasks],
                'Priority': [t.priority.value for t in tasks],
                'Created': [t.created_at.strftime('%Y-%m-%d') for t in tasks],
                'Completed': [t.completed for t in tasks],
            }
            df_tasks = pd.DataFrame(tasks_data)
            df_tasks.to_excel(writer, sheet_name='Tasks', index=False)

        # Risks sheet
        if risks:
            risks_data = {
                'ID': [r.id for r in risks],
                'Title': [r.title for r in risks],
                'Severity': [r.severity.value for r in risks],
                'Probability': [r.probability.value for r in risks],
                'Impact': [r.impact.value for r in risks],
                'Status': [r.status.value for r in risks],
                'Created': [r.created_at.strftime('%Y-%m-%d') for r in risks],
            }
            df_risks = pd.DataFrame(risks_data)
            df_risks.to_excel(writer, sheet_name='Risks', index=False)

        # Projects sheet
        if projects:
            projects_data = {
                'ID': [p.id for p in projects],
                'Name': [p.name for p in projects],
                'Status': [p.status.value for p in projects],
                'Progress': [f"{p.progress:.0f}%" for p in projects],
                'Created': [p.created_at.strftime('%Y-%m-%d') for p in projects],
            }
            df_projects = pd.DataFrame(projects_data)
            df_projects.to_excel(writer, sheet_name='Projects', index=False)

        # Velocity sheet
        if analytics.velocity_data:
            velocity_data = {
                'Week': [v.week for v in analytics.velocity_data],
                'Tasks Completed': [v.tasks_completed for v in analytics.velocity_data],
                'Average': [v.average for v in analytics.velocity_data],
            }
            df_velocity = pd.DataFrame(velocity_data)
            df_velocity.to_excel(writer, sheet_name='Velocity', index=False)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=analytics_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"}
    )
