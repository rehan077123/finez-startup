"use client";

import { useState } from "react";
import { Search, Mic } from "lucide-react";
import { Input } from "@/components/ui";

interface SearchBarProps {
  onSearch?: (query: string) => void;
  placeholder?: string;
  enableVoice?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = "Describe what you're looking for...",
  enableVoice = false,
}) => {
  const [query, setQuery] = useState("");
  const [isListening, setIsListening] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch?.(query);
    }
  };

  const handleVoiceSearch = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in your browser");
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    setIsListening(true);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      onSearch?.(transcript);
    };

    recognition.onerror = () => {
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <form onSubmit={handleSearch} className="w-full">
      <div className="relative flex gap-2">
        <Input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="flex-1 pl-12"
        />
        <button
          type="submit"
          className="absolute left-4 top-1/2 transform -translate-y-1/2 text-blue-600 hover:text-blue-700"
        >
          <Search size={20} />
        </button>

        {enableVoice && (
          <button
            type="button"
            onClick={handleVoiceSearch}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              isListening
                ? "bg-red-600 text-white"
                : "bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600"
            }`}
          >
            <Mic size={18} />
          </button>
        )}
      </div>
    </form>
  );
};
