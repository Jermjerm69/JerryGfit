"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bot, Wand2, Copy, Download, RotateCcw, Loader2 } from "lucide-react";
import { aiAPI } from "@/lib/api";
import { toast } from "@/components/providers/toast-provider";

const AI_MODELS = [
  { value: "gpt-4", label: "GPT-4" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
  { value: "claude-3", label: "Claude 3" },
  { value: "gemini-pro", label: "Gemini Pro" },
];

const PROMPT_TEMPLATES = [
  {
    name: "Workout Caption",
    prompt:
      "Generate an inspiring and motivational fitness caption for a workout post about:",
    type: "caption",
  },
  {
    name: "Fitness Hashtags",
    prompt:
      "Create trending fitness hashtags for a social media post about:",
    type: "hashtag",
  },
  {
    name: "Workout Plan",
    prompt:
      "Design a detailed workout plan with exercises, sets, reps, and rest times for:",
    type: "workout_plan",
  },
  {
    name: "Fitness Tips",
    prompt: "Provide expert fitness and nutrition tips for:",
    type: "content",
  },
];

interface GeneratedResult {
  id: string;
  content: string;
  timestamp: Date;
}

export default function AIStudioPage() {
  const [prompt, setPrompt] = useState("");
  const [selectedModel, setSelectedModel] = useState("gpt-4");
  const [outputCount, setOutputCount] = useState(1);
  const [results, setResults] = useState<GeneratedResult[]>([]);
  const [selectedTemplateType, setSelectedTemplateType] = useState<string>("content");

  const queryClient = useQueryClient();

  // Fetch AI history from database
  const { data: aiHistory = [], isLoading: historyLoading } = useQuery({
    queryKey: ['ai-history'],
    queryFn: () => aiAPI.getHistory(),
  });

  // AI generation mutation
  const generateMutation = useMutation({
    mutationFn: (request: { prompt: string; model: string; type: string }) =>
      aiAPI.generate({
        request_type: request.type,
        prompt: request.prompt,
        model: request.model,
      }),
    onSuccess: (data) => {
      // Format the generated content nicely
      let formattedContent = "";
      if (Array.isArray(data.data)) {
        formattedContent = data.data.map((item: { content?: string }) => item.content || JSON.stringify(item)).join("\n\n");
      } else {
        formattedContent = JSON.stringify(data.data, null, 2);
      }

      // Add generated result to display
      const newResult: GeneratedResult = {
        id: `${Date.now()}`,
        content: formattedContent,
        timestamp: new Date(),
      };
      setResults([newResult, ...results]);

      // Refresh AI history
      queryClient.invalidateQueries({ queryKey: ['ai-history'] });

      toast.success('Content generated successfully!');
    },
    onError: (error: { response?: { data?: { detail?: string } } }) => {
      toast.error(error.response?.data?.detail || 'Failed to generate content');
    },
  });

  const handleTemplateSelect = (template: typeof PROMPT_TEMPLATES[0]) => {
    setPrompt(template.prompt);
    setSelectedTemplateType(template.type);
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    generateMutation.mutate({
      prompt: prompt,
      model: selectedModel,
      type: selectedTemplateType,
    });
  };

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content);
    toast.success('Copied to clipboard!');
  };

  const handleExport = () => {
    const exportData = {
      prompt,
      model: selectedModel,
      results,
      exportedAt: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ai-studio-export-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleClear = () => {
    setPrompt("");
    setResults([]);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Bot className="h-8 w-8" />
          AI Studio
        </h1>
        <p className="text-muted-foreground">
          Generate workout captions, fitness hashtags, training plans, and get AI-powered fitness coaching insights.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="model">AI Model</Label>
                  <Select value={selectedModel} onValueChange={setSelectedModel}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a model" />
                    </SelectTrigger>
                    <SelectContent>
                      {AI_MODELS.map((model) => (
                        <SelectItem key={model.value} value={model.value}>
                          {model.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="outputs">Number of Outputs</Label>
                  <Input
                    id="outputs"
                    type="number"
                    min="1"
                    max="5"
                    value={outputCount}
                    onChange={(e) => setOutputCount(parseInt(e.target.value) || 1)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Quick Templates</Label>
                <div className="flex flex-wrap gap-2">
                  {PROMPT_TEMPLATES.map((template) => (
                    <Button
                      key={template.name}
                      variant="outline"
                      size="sm"
                      onClick={() => handleTemplateSelect(template)}
                    >
                      {template.name}
                    </Button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="prompt">Prompt</Label>
                <Textarea
                  id="prompt"
                  placeholder="Enter your prompt here... Be specific about what you want the AI to generate."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={8}
                />
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handleGenerate}
                  disabled={!prompt.trim() || generateMutation.isPending}
                  className="flex-1"
                >
                  {generateMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-4 w-4 mr-2" />
                      Generate
                    </>
                  )}
                </Button>
                <Button variant="outline" onClick={handleClear}>
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Clear
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Generation History</CardTitle>
            </CardHeader>
            <CardContent>
              {historyLoading ? (
                <div className="flex justify-center py-4">
                  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                </div>
              ) : (
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Total Generations:</span>
                    <span className="font-medium">{aiHistory.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>This Session:</span>
                    <span className="font-medium">{results.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Current Model:</span>
                    <span className="font-medium">
                      {AI_MODELS.find(m => m.value === selectedModel)?.label}
                    </span>
                  </div>
                  <div className="mt-4 pt-4 border-t">
                    <h4 className="font-medium mb-2">Recent Activity</h4>
                    <div className="space-y-2">
                      {aiHistory.slice(0, 5).map((item) => (
                        <div key={item.id} className="text-xs p-2 bg-muted/50 rounded">
                          <div className="font-medium capitalize">{item.request_type}</div>
                          <div className="text-muted-foreground truncate">
                            {item.prompt.substring(0, 50)}...
                          </div>
                          <div className="text-muted-foreground mt-1">
                            {item.tokens_used} tokens
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {results.length > 0 && (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Generated Results</CardTitle>
            <Button variant="outline" size="sm" onClick={handleExport}>
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </CardHeader>
          <CardContent className="space-y-6">
            {results.map((result, index) => (
              <div
                key={result.id}
                className="border rounded-lg p-4 space-y-3 bg-muted/30"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">Output {index + 1}</h4>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">
                      {result.timestamp.toLocaleTimeString()}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleCopy(result.content)}
                    >
                      <Copy className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="whitespace-pre-wrap text-sm bg-background p-3 rounded border">
                  {result.content}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {aiHistory.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Previous AI Generations</CardTitle>
            <p className="text-sm text-muted-foreground">
              Your complete AI generation history
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            {aiHistory.map((item) => (
              <div
                key={item.id}
                className="border rounded-lg p-4 space-y-3 bg-muted/30"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium capitalize">{item.request_type}</h4>
                    <p className="text-xs text-muted-foreground">
                      {new Date(item.created_at).toLocaleString()} • {item.tokens_used} tokens
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleCopy((item.response as { content?: string })?.content || JSON.stringify(item.response))}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>
                <div className="text-sm">
                  <div className="font-medium mb-1">Prompt:</div>
                  <div className="text-muted-foreground bg-background p-2 rounded border">
                    {item.prompt}
                  </div>
                </div>
                <div className="text-sm">
                  <div className="font-medium mb-1">Response:</div>
                  <div className="whitespace-pre-wrap text-muted-foreground bg-background p-3 rounded border">
                    {(item.response as { content?: string }) ?.content || JSON.stringify(item.response, null, 2)}
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}