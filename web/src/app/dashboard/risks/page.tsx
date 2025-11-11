"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertCircle,
  Plus,
  Edit,
  Trash2,
  Shield,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Loader2,
  Search,
} from "lucide-react";
import { risksAPI, Risk, RiskCreate, RiskUpdate } from "@/lib/api";
import { toast } from "@/components/providers/toast-provider";

type RiskFormData = {
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  probability: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'mitigated' | 'closed';
  mitigation_plan: string;
};

const initialFormData: RiskFormData = {
  title: '',
  description: '',
  severity: 'medium',
  probability: 'medium',
  impact: 'medium',
  status: 'open',
  mitigation_plan: '',
};

export default function RisksPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRisk, setEditingRisk] = useState<Risk | null>(null);
  const [formData, setFormData] = useState<RiskFormData>(initialFormData);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSeverity, setFilterSeverity] = useState<string>('all');

  const queryClient = useQueryClient();

  // Fetch all risks
  const { data: risks = [], isLoading } = useQuery({
    queryKey: ['risks'],
    queryFn: () => risksAPI.getAll(0, 1000),
  });

  // Create risk mutation
  const createMutation = useMutation({
    mutationFn: (data: RiskCreate) => risksAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['risks'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      setIsModalOpen(false);
      setFormData(initialFormData);
      toast.success('Risk created successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create risk');
    },
  });

  // Update risk mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: RiskUpdate }) =>
      risksAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['risks'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      setIsModalOpen(false);
      setEditingRisk(null);
      setFormData(initialFormData);
      toast.success('Risk updated successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update risk');
    },
  });

  // Delete risk mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => risksAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['risks'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      toast.success('Risk deleted successfully!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete risk');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      toast.error('Please enter a risk title');
      return;
    }

    if (editingRisk) {
      updateMutation.mutate({ id: editingRisk.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleEdit = (risk: Risk) => {
    setEditingRisk(risk);
    setFormData({
      title: risk.title,
      description: risk.description || '',
      severity: risk.severity,
      probability: risk.probability,
      impact: risk.impact,
      status: risk.status,
      mitigation_plan: risk.mitigation_plan || '',
    });
    setIsModalOpen(true);
  };

  const handleDelete = (id: number) => {
    if (confirm('Are you sure you want to delete this risk?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleOpenModal = () => {
    setEditingRisk(null);
    setFormData(initialFormData);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingRisk(null);
    setFormData(initialFormData);
  };

  // Filter risks
  const filteredRisks = risks.filter((risk) => {
    const matchesSearch = risk.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      risk.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || risk.status === filterStatus;
    const matchesSeverity = filterSeverity === 'all' || risk.severity === filterSeverity;
    return matchesSearch && matchesStatus && matchesSeverity;
  });

  // Helper functions for badge colors
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-red-100 text-red-800 border-red-200';
      case 'mitigated': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'closed': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <AlertCircle className="h-4 w-4" />;
      case 'mitigated': return <CheckCircle2 className="h-4 w-4" />;
      case 'closed': return <XCircle className="h-4 w-4" />;
      default: return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getRiskScore = (probability: string, impact: string) => {
    const probValue = { low: 1, medium: 2, high: 3 }[probability] || 2;
    const impactValue = { low: 1, medium: 2, high: 3, critical: 4 }[impact] || 2;
    return probValue * impactValue;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Shield className="h-8 w-8" />
            Risk Register
          </h1>
          <p className="text-muted-foreground">
            Identify, assess, and manage project risks
          </p>
        </div>
        <Button onClick={handleOpenModal}>
          <Plus className="h-4 w-4 mr-2" />
          Add Risk
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Risks</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{risks.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Open</CardTitle>
            <AlertCircle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {risks.filter(r => r.status === 'open').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Mitigated</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {risks.filter(r => r.status === 'mitigated').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {risks.filter(r => r.severity === 'critical').length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4 flex-wrap">
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search risks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9"
                />
              </div>
            </div>
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="open">Open</SelectItem>
                <SelectItem value="mitigated">Mitigated</SelectItem>
                <SelectItem value="closed">Closed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterSeverity} onValueChange={setFilterSeverity}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by severity" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Severity</SelectItem>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="critical">Critical</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Risks Table */}
      <Card>
        <CardHeader>
          <CardTitle>Risks ({filteredRisks.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredRisks.length === 0 ? (
              <div className="text-center py-12">
                <Shield className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">
                  {searchTerm || filterStatus !== 'all' || filterSeverity !== 'all'
                    ? 'No risks match your filters'
                    : 'No risks yet. Add your first risk to get started.'}
                </p>
              </div>
            ) : (
              filteredRisks.map((risk) => (
                <div
                  key={risk.id}
                  className="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-semibold text-lg">{risk.title}</h3>
                        <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(risk.status)} flex items-center gap-1`}>
                          {getStatusIcon(risk.status)}
                          {risk.status.toUpperCase()}
                        </span>
                      </div>
                      {risk.description && (
                        <p className="text-sm text-muted-foreground mb-3">
                          {risk.description}
                        </p>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEdit(risk)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(risk.id)}
                        disabled={deleteMutation.isPending}
                      >
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                    <div>
                      <Label className="text-xs text-muted-foreground">Severity</Label>
                      <div className={`text-xs px-2 py-1 rounded border inline-block mt-1 ${getSeverityColor(risk.severity)}`}>
                        {risk.severity.toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground">Probability</Label>
                      <div className={`text-xs px-2 py-1 rounded border inline-block mt-1 ${getSeverityColor(risk.probability)}`}>
                        {risk.probability.toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground">Impact</Label>
                      <div className={`text-xs px-2 py-1 rounded border inline-block mt-1 ${getSeverityColor(risk.impact)}`}>
                        {risk.impact.toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground">Risk Score</Label>
                      <div className="text-sm font-bold mt-1">
                        {getRiskScore(risk.probability, risk.impact)} / 12
                      </div>
                    </div>
                  </div>

                  {risk.mitigation_plan && (
                    <div className="bg-muted/50 rounded p-3 mt-3">
                      <Label className="text-xs text-muted-foreground">Mitigation Plan</Label>
                      <p className="text-sm mt-1">{risk.mitigation_plan}</p>
                    </div>
                  )}

                  <div className="flex gap-4 text-xs text-muted-foreground mt-3">
                    <span>Created: {new Date(risk.created_at).toLocaleDateString()}</span>
                    <span>Updated: {new Date(risk.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Add/Edit Risk Modal */}
      <Dialog open={isModalOpen} onOpenChange={handleCloseModal}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {editingRisk ? 'Edit Risk' : 'Add New Risk'}
            </DialogTitle>
            <DialogDescription>
              Fill in the risk details below. All fields marked with * are required.
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="title">Risk Title *</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="e.g., Database server downtime"
                required
              />
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Describe the risk in detail..."
                rows={3}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="severity">Severity *</Label>
                <Select
                  value={formData.severity}
                  onValueChange={(value: any) => setFormData({ ...formData, severity: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="critical">Critical</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="status">Status *</Label>
                <Select
                  value={formData.status}
                  onValueChange={(value: any) => setFormData({ ...formData, status: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="open">Open</SelectItem>
                    <SelectItem value="mitigated">Mitigated</SelectItem>
                    <SelectItem value="closed">Closed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="probability">Probability *</Label>
                <Select
                  value={formData.probability}
                  onValueChange={(value: any) => setFormData({ ...formData, probability: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low (1)</SelectItem>
                    <SelectItem value="medium">Medium (2)</SelectItem>
                    <SelectItem value="high">High (3)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="impact">Impact *</Label>
                <Select
                  value={formData.impact}
                  onValueChange={(value: any) => setFormData({ ...formData, impact: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low (1)</SelectItem>
                    <SelectItem value="medium">Medium (2)</SelectItem>
                    <SelectItem value="high">High (3)</SelectItem>
                    <SelectItem value="critical">Critical (4)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="bg-muted p-3 rounded">
              <Label className="text-xs">Risk Score (Probability × Impact)</Label>
              <div className="text-2xl font-bold mt-1">
                {getRiskScore(formData.probability, formData.impact)} / 12
              </div>
            </div>

            <div>
              <Label htmlFor="mitigation_plan">Mitigation Plan</Label>
              <Textarea
                id="mitigation_plan"
                value={formData.mitigation_plan}
                onChange={(e) => setFormData({ ...formData, mitigation_plan: e.target.value })}
                placeholder="How will you mitigate or respond to this risk?"
                rows={4}
              />
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={handleCloseModal}>
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={createMutation.isPending || updateMutation.isPending}
              >
                {createMutation.isPending || updateMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : editingRisk ? (
                  'Update Risk'
                ) : (
                  'Create Risk'
                )}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
