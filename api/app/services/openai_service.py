"""OpenAI service for AI content generation."""

from typing import Any, Dict, List, Optional
import openai
from openai import OpenAI, OpenAIError, APIError, RateLimitError, APIConnectionError
import logging

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


class OpenAIService:
    """Service for handling OpenAI API interactions."""

    def __init__(self):
        if not client:
            logger.warning("OpenAI API key not configured. AI features will be disabled.")
        self.client = client

    def _make_request(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Make a request to OpenAI API with error handling.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: OpenAI model to use (default: gpt-4)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with 'content' and 'tokens_used'

        Raises:
            ValueError: If API key is not configured
            Exception: For various OpenAI API errors
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            return {
                "content": content,
                "tokens_used": tokens_used,
            }

        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise Exception("AI service is currently at capacity. Please try again in a few moments.")

        except APIConnectionError as e:
            logger.error(f"OpenAI API connection error: {e}")
            raise Exception("Unable to connect to AI service. Please check your internet connection and try again.")

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"AI service error: {str(e)}")

        except OpenAIError as e:
            logger.error(f"OpenAI error: {e}")
            raise Exception(f"An error occurred with the AI service: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error in OpenAI request: {e}")
            raise Exception("An unexpected error occurred. Please try again.")

    def generate_fitness_caption(
        self,
        context: str,
        tone: str = "motivational",
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate a fitness-themed social media caption.

        Args:
            context: Context or topic for the caption
            tone: Tone of the caption (motivational, educational, casual)
            model: OpenAI model to use

        Returns:
            Dictionary with generated content and token usage
        """
        system_prompt = (
            "You are a professional fitness content creator. "
            "Generate engaging, authentic, and inspiring social media captions "
            "for fitness and wellness content. Keep captions concise (2-4 sentences) "
            "and include relevant emojis where appropriate."
        )

        user_prompt = (
            f"Create a {tone} fitness caption about: {context}\n\n"
            f"The caption should be inspiring, relatable, and encourage action."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=200)

        return {
            "type": "fitness_caption",
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }

    def generate_hashtags(
        self,
        caption: str,
        niche: str = "fitness",
        count: int = 15,
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate relevant hashtags for social media posts.

        Args:
            caption: The caption or content to generate hashtags for
            niche: The niche or topic area
            count: Number of hashtags to generate
            model: OpenAI model to use

        Returns:
            Dictionary with generated hashtags and token usage
        """
        system_prompt = (
            "You are a social media growth expert. "
            "Generate highly relevant, trending hashtags that will maximize reach and engagement. "
            "Focus on a mix of broad and niche-specific tags."
        )

        user_prompt = (
            f"Generate {count} effective hashtags for this {niche} post:\n\n"
            f"{caption}\n\n"
            f"Return only the hashtags separated by spaces, starting with #."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=150)

        return {
            "type": "hashtags",
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }

    def generate_workout_plan(
        self,
        goal: str,
        level: str = "intermediate",
        duration: str = "30 minutes",
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate a detailed workout plan.

        Args:
            goal: Fitness goal (e.g., "build muscle", "lose weight")
            level: Fitness level (beginner, intermediate, advanced)
            duration: Workout duration
            model: OpenAI model to use

        Returns:
            Dictionary with generated workout plan and token usage
        """
        system_prompt = (
            "You are a certified personal trainer with expertise in creating "
            "safe, effective workout programs. Provide structured workout plans "
            "with exercises, sets, reps, and rest periods."
        )

        user_prompt = (
            f"Create a {duration} {level} workout plan for someone who wants to {goal}.\n\n"
            f"Include:\n"
            f"- Warm-up exercises\n"
            f"- Main workout with sets/reps/rest\n"
            f"- Cool-down/stretching\n"
            f"- Safety tips"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=800)

        return {
            "type": "workout_plan",
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }

    def generate_project_risks(
        self,
        project_description: str,
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate potential project risks with mitigation strategies.

        Args:
            project_description: Description of the project
            model: OpenAI model to use

        Returns:
            Dictionary with list of risks and token usage
        """
        system_prompt = (
            "You are a project management expert. Analyze projects and identify "
            "potential risks with their probability, impact, and mitigation strategies. "
            "Return your response as a JSON array of risk objects."
        )

        user_prompt = (
            f"Analyze this project and identify 3-5 key risks:\n\n"
            f"{project_description}\n\n"
            f"For each risk, provide:\n"
            f"- title: Brief risk title\n"
            f"- description: Detailed risk description\n"
            f"- severity: LOW, MEDIUM, HIGH, or CRITICAL\n"
            f"- mitigation_plan: How to mitigate this risk\n\n"
            f"Format as JSON array."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=1000)

        return {
            "type": "project_risks",
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }

    def generate_task_breakdown(
        self,
        project_goal: str,
        timeframe: str = "2 weeks",
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate a task breakdown for a project.

        Args:
            project_goal: The project goal or description
            timeframe: Project timeframe
            model: OpenAI model to use

        Returns:
            Dictionary with task list and token usage
        """
        system_prompt = (
            "You are a project management expert. Break down projects into "
            "actionable tasks with priorities and realistic timelines. "
            "Return response as JSON array of task objects."
        )

        user_prompt = (
            f"Break down this project goal into 4-7 specific tasks:\n\n"
            f"Goal: {project_goal}\n"
            f"Timeframe: {timeframe}\n\n"
            f"For each task provide:\n"
            f"- title: Task name\n"
            f"- description: What needs to be done\n"
            f"- priority: LOW, MEDIUM, HIGH, or URGENT\n"
            f"- estimated_days: Number of days to complete\n\n"
            f"Format as JSON array."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=1000)

        return {
            "type": "task_breakdown",
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }

    def generate_general_content(
        self,
        request_type: str,
        prompt: str,
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """
        Generate general AI content based on custom prompts.

        Args:
            request_type: Type of content being requested
            prompt: User's prompt
            model: OpenAI model to use

        Returns:
            Dictionary with generated content and token usage
        """
        system_prompt = (
            "You are a helpful AI assistant specializing in fitness, wellness, "
            "and project management. Provide accurate, actionable, and inspiring content."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        result = self._make_request(messages, model=model, max_tokens=800)

        return {
            "type": request_type,
            "content": result["content"],
            "tokens_used": result["tokens_used"],
        }


# Create a singleton instance
openai_service = OpenAIService()
