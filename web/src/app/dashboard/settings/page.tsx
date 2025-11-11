"use client";

import { useState, useEffect, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAuth } from "@/contexts/AuthContext";
import api from "@/lib/api";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import {
  Settings,
  User,
  Bell,
  Shield,
  Palette,
  Save,
  Upload,
  Loader2,
  Check,
  Download,
  Trash2,
  AlertTriangle,
} from "lucide-react";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("profile");
  const { user, logout, isLoading } = useAuth();
  const queryClient = useQueryClient();
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [profilePictureUrl, setProfilePictureUrl] = useState<string | null>(null);

  // Show loading state while user data is being fetched
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin mx-auto" />
          <p className="text-muted-foreground">Loading settings...</p>
        </div>
      </div>
    );
  }

  // Redirect if not authenticated
  if (!user) {
    router.push('/auth/login');
    return null;
  }

  const [profile, setProfile] = useState({
    full_name: user?.full_name || "",
    email: user?.email || "",
    username: user?.username || "",
  });

  const [passwordData, setPasswordData] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [deletePassword, setDeletePassword] = useState("");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Update profile state when user data loads
  useEffect(() => {
    if (user) {
      setProfile({
        full_name: user.full_name || "",
        email: user.email || "",
        username: user.username || "",
      });
      // Construct full URL for profile picture
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const baseUrl = apiUrl.replace('/api/v1', '');
      setProfilePictureUrl(user.profile_picture ? `${baseUrl}/${user.profile_picture}` : null);
      if (user.notification_preferences) {
        setNotifications(user.notification_preferences);
      }
      if (user.user_preferences) {
        setPreferences(user.user_preferences);
      }
    }
  }, [user]);

  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    pushNotifications: false,
    taskReminders: true,
    weeklyReports: true,
    riskAlerts: true,
  });

  const [preferences, setPreferences] = useState({
    language: "english",
    dateFormat: "MM/DD/YYYY",
    timeFormat: "12-hour",
  });

  const handleProfileChange = (field: string, value: string) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const handleNotificationChange = (field: string, value: boolean) => {
    setNotifications((prev) => ({ ...prev, [field]: value }));
  };

  const handlePreferenceChange = (field: string, value: string | boolean) => {
    setPreferences((prev) => ({ ...prev, [field]: value }));
  };

  // Mutation for updating user profile
  const updateProfileMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.put('/users/me', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
      setSaveSuccess(true);
      toast.success("Profile updated successfully!");
      setTimeout(() => setSaveSuccess(false), 3000);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to update profile");
    },
  });

  // Mutation for photo upload
  const uploadPhotoMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const response = await api.post('/users/me/upload-photo', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
      // Construct full URL for profile picture
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const baseUrl = apiUrl.replace('/api/v1', '');
      setProfilePictureUrl(data.file_path ? `${baseUrl}/${data.file_path}` : null);
      toast.success("Profile picture uploaded successfully!");
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to upload photo");
    },
  });

  // Mutation for password change
  const changePasswordMutation = useMutation({
    mutationFn: async (data: { current_password: string; new_password: string }) => {
      const response = await api.post('/users/me/change-password', data);
      return response.data;
    },
    onSuccess: () => {
      toast.success("Password changed successfully!");
      setPasswordData({ current_password: "", new_password: "", confirm_password: "" });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to change password");
    },
  });

  // Mutation for exporting data
  const exportDataMutation = useMutation({
    mutationFn: async () => {
      const response = await api.get('/users/me/export');
      return response.data;
    },
    onSuccess: (data) => {
      // Download as JSON file
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `jerrygfit_export_${new Date().toISOString()}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success("Account data exported successfully!");
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to export data");
    },
  });

  // Mutation for deleting account
  const deleteAccountMutation = useMutation({
    mutationFn: async (password: string) => {
      const response = await api.delete('/users/me', { data: { password } });
      return response.data;
    },
    onSuccess: () => {
      toast.success("Account deleted successfully");
      logout();
      router.push('/auth/login');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to delete account");
    },
  });

  const handleSaveProfile = () => {
    updateProfileMutation.mutate(profile);
  };

  const handleSaveNotifications = () => {
    updateProfileMutation.mutate({ notification_preferences: notifications });
  };

  const handleSavePreferences = () => {
    updateProfileMutation.mutate({ user_preferences: preferences });
  };

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (2MB)
      if (file.size > 2 * 1024 * 1024) {
        toast.error("File size must be less than 2MB");
        return;
      }
      // Validate file type
      if (!['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type)) {
        toast.error("Only JPG, PNG, GIF, and WEBP files are allowed");
        return;
      }
      uploadPhotoMutation.mutate(file);
    }
  };

  const handlePasswordChange = () => {
    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error("New passwords do not match");
      return;
    }
    if (passwordData.new_password.length < 8) {
      toast.error("Password must be at least 8 characters long");
      return;
    }
    changePasswordMutation.mutate({
      current_password: passwordData.current_password,
      new_password: passwordData.new_password,
    });
  };

  const handleExportData = () => {
    exportDataMutation.mutate();
  };

  const handleDeleteAccount = () => {
    if (!deletePassword) {
      toast.error("Please enter your password to confirm");
      return;
    }
    deleteAccountMutation.mutate(deletePassword);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Settings className="h-8 w-8" />
          Settings
        </h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="profile" isActive={activeTab === "profile"} onClick={() => setActiveTab("profile")}>
            <User className="h-4 w-4 mr-2" />
            Profile
          </TabsTrigger>
          <TabsTrigger value="notifications" isActive={activeTab === "notifications"} onClick={() => setActiveTab("notifications")}>
            <Bell className="h-4 w-4 mr-2" />
            Notifications
          </TabsTrigger>
          <TabsTrigger value="appearance" isActive={activeTab === "appearance"} onClick={() => setActiveTab("appearance")}>
            <Palette className="h-4 w-4 mr-2" />
            Appearance
          </TabsTrigger>
          <TabsTrigger value="security" isActive={activeTab === "security"} onClick={() => setActiveTab("security")}>
            <Shield className="h-4 w-4 mr-2" />
            Security
          </TabsTrigger>
        </TabsList>

        <TabsContent value="profile" activeValue={activeTab}>
          <div className="grid gap-6 md:grid-cols-3">
            <div className="md:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Profile Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="full_name">Full Name</Label>
                      <Input
                        id="full_name"
                        value={profile.full_name}
                        onChange={(e) =>
                          handleProfileChange("full_name", e.target.value)
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="username">Username</Label>
                      <Input
                        id="username"
                        value={profile.username}
                        onChange={(e) =>
                          handleProfileChange("username", e.target.value)
                        }
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={profile.email}
                      onChange={(e) =>
                        handleProfileChange("email", e.target.value)
                      }
                    />
                  </div>

                  {saveSuccess && (
                    <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
                      <Check className="h-4 w-4" />
                      <span>Profile updated successfully!</span>
                    </div>
                  )}

                  <Button onClick={handleSaveProfile} disabled={updateProfileMutation.isPending}>
                    {updateProfileMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="h-4 w-4 mr-2" />
                        Save Changes
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </div>

            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Profile Picture</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-center h-32 w-32 mx-auto bg-muted rounded-full overflow-hidden">
                    {profilePictureUrl ? (
                      <img src={profilePictureUrl} alt="Profile" className="w-full h-full object-cover" />
                    ) : (
                      <User className="h-16 w-16 text-muted-foreground" />
                    )}
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/jpeg,image/png,image/gif,image/webp"
                    onChange={handlePhotoUpload}
                    className="hidden"
                  />
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={uploadPhotoMutation.isPending}
                  >
                    {uploadPhotoMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Uploading...
                      </>
                    ) : (
                      <>
                        <Upload className="h-4 w-4 mr-2" />
                        Upload Photo
                      </>
                    )}
                  </Button>
                  <p className="text-xs text-muted-foreground text-center">
                    JPG, PNG, GIF or WEBP. Max size 2MB.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="notifications" activeValue={activeTab}>
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Email Notifications</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive notifications via email
                  </p>
                </div>
                <Switch
                  checked={notifications.emailNotifications}
                  onCheckedChange={(checked) =>
                    handleNotificationChange("emailNotifications", checked)
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Push Notifications</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive push notifications in your browser
                  </p>
                </div>
                <Switch
                  checked={notifications.pushNotifications}
                  onCheckedChange={(checked) =>
                    handleNotificationChange("pushNotifications", checked)
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Task Reminders</Label>
                  <p className="text-sm text-muted-foreground">
                    Get reminded about upcoming task deadlines
                  </p>
                </div>
                <Switch
                  checked={notifications.taskReminders}
                  onCheckedChange={(checked) =>
                    handleNotificationChange("taskReminders", checked)
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Weekly Reports</Label>
                  <p className="text-sm text-muted-foreground">
                    Receive weekly project progress reports
                  </p>
                </div>
                <Switch
                  checked={notifications.weeklyReports}
                  onCheckedChange={(checked) =>
                    handleNotificationChange("weeklyReports", checked)
                  }
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <Label>Risk Alerts</Label>
                  <p className="text-sm text-muted-foreground">
                    Get notified about high-priority risks
                  </p>
                </div>
                <Switch
                  checked={notifications.riskAlerts}
                  onCheckedChange={(checked) =>
                    handleNotificationChange("riskAlerts", checked)
                  }
                />
              </div>

              <Button onClick={handleSaveNotifications} disabled={updateProfileMutation.isPending}>
                {updateProfileMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Save Preferences
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="appearance" activeValue={activeTab}>
          <Card>
            <CardHeader>
              <CardTitle>Appearance Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Language</Label>
                <Input
                  value={preferences.language}
                  onChange={(e) =>
                    handlePreferenceChange("language", e.target.value)
                  }
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Date Format</Label>
                  <Input
                    value={preferences.dateFormat}
                    onChange={(e) =>
                      handlePreferenceChange("dateFormat", e.target.value)
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label>Time Format</Label>
                  <Input
                    value={preferences.timeFormat}
                    onChange={(e) =>
                      handlePreferenceChange("timeFormat", e.target.value)
                    }
                  />
                </div>
              </div>

              <Button onClick={handleSavePreferences} disabled={updateProfileMutation.isPending}>
                {updateProfileMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Save Preferences
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" activeValue={activeTab}>
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Change Password</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="current-password">Current Password</Label>
                  <Input
                    id="current-password"
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) =>
                      setPasswordData({ ...passwordData, current_password: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="new-password">New Password</Label>
                  <Input
                    id="new-password"
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) =>
                      setPasswordData({ ...passwordData, new_password: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirm-password">Confirm New Password</Label>
                  <Input
                    id="confirm-password"
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={(e) =>
                      setPasswordData({ ...passwordData, confirm_password: e.target.value })
                    }
                  />
                </div>
                <Button onClick={handlePasswordChange} disabled={changePasswordMutation.isPending}>
                  {changePasswordMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Updating...
                    </>
                  ) : (
                    "Update Password"
                  )}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Account Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={handleExportData}
                    disabled={exportDataMutation.isPending}
                  >
                    {exportDataMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Exporting...
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4 mr-2" />
                        Export Account Data
                      </>
                    )}
                  </Button>

                  {!showDeleteConfirm ? (
                    <Button
                      variant="destructive"
                      className="w-full"
                      onClick={() => setShowDeleteConfirm(true)}
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Delete Account
                    </Button>
                  ) : (
                    <div className="space-y-3 p-4 border-2 border-destructive rounded-lg bg-destructive/5">
                      <div className="flex items-center gap-2 text-destructive">
                        <AlertTriangle className="h-5 w-5" />
                        <span className="font-semibold">This action cannot be undone!</span>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        All your data including tasks, risks, projects, and posts will be permanently deleted.
                      </p>
                      <Input
                        type="password"
                        placeholder="Enter your password to confirm"
                        value={deletePassword}
                        onChange={(e) => setDeletePassword(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          className="flex-1"
                          onClick={() => {
                            setShowDeleteConfirm(false);
                            setDeletePassword("");
                          }}
                        >
                          Cancel
                        </Button>
                        <Button
                          variant="destructive"
                          className="flex-1"
                          onClick={handleDeleteAccount}
                          disabled={deleteAccountMutation.isPending}
                        >
                          {deleteAccountMutation.isPending ? (
                            <>
                              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                              Deleting...
                            </>
                          ) : (
                            <>
                              <Trash2 className="h-4 w-4 mr-2" />
                              Confirm Delete
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
