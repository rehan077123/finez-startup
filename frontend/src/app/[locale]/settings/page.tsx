"use client";

import { useState } from "react";
import { Card, Button, Input, Switch } from "@/components/ui";
import { User, Bell, Lock, Palette } from "lucide-react";

export default function SettingsPage() {
  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    pushNotifications: false,
    darkMode: true,
    twoFactor: false,
  });

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Settings
      </h1>

      {/* Account Settings */}
      <Card className="p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <User size={20} />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Account
          </h2>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Email
            </label>
            <Input value="user@example.com" disabled />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Full Name
            </label>
            <Input defaultValue="John Doe" />
          </div>
          <Button>Update Profile</Button>
        </div>
      </Card>

      {/* Notification Settings */}
      <Card className="p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <Bell size={20} />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Notifications
          </h2>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-900 dark:text-white">
              Email Notifications
            </span>
            <Switch
              checked={preferences.emailNotifications}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  emailNotifications: e.target.checked,
                })
              }
            />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-900 dark:text-white">
              Push Notifications
            </span>
            <Switch
              checked={preferences.pushNotifications}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  pushNotifications: e.target.checked,
                })
              }
            />
          </div>
        </div>
      </Card>

      {/* Appearance */}
      <Card className="p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <Palette size={20} />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Appearance
          </h2>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-900 dark:text-white">Dark Mode</span>
          <Switch
            checked={preferences.darkMode}
            onChange={(e) =>
              setPreferences({
                ...preferences,
                darkMode: e.target.checked,
              })
            }
          />
        </div>
      </Card>

      {/* Security */}
      <Card className="p-6 mb-6">
        <div className="flex items-center gap-3 mb-4">
          <Lock size={20} />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Security
          </h2>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-900 dark:text-white">
            Two-Factor Authentication
          </span>
          <Switch
            checked={preferences.twoFactor}
            onChange={(e) =>
              setPreferences({
                ...preferences,
                twoFactor: e.target.checked,
              })
            }
          />
        </div>
      </Card>
    </div>
  );
}
