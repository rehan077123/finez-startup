"use client";

import { Modal, Button, RadioGroup } from "@/components/ui";
import { useState } from "react";

interface AmbiguityModalProps {
  isOpen: boolean;
  query: string;
  options: Array<{
    value: string;
    label: string;
    description?: string;
  }>;
  onSelect?: (value: string) => void;
  onSkip?: () => void;
}

export const AmbiguityModal: React.FC<AmbiguityModalProps> = ({
  isOpen,
  query,
  options,
  onSelect,
  onSkip,
}) => {
  const [selected, setSelected] = useState<string>("");

  const handleSelect = () => {
    if (selected) {
      onSelect?.(selected);
      setSelected("");
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onSkip || (() => {})} title="Clarify Your Search">
      <div className="space-y-6">
        <p className="text-gray-600 dark:text-gray-400">
          We found multiple interpretations for "{query}". Which one were you looking for?
        </p>

        <RadioGroup
          name="ambiguity"
          options={options}
          value={selected}
          onChange={setSelected}
        />

        <div className="flex gap-3 justify-end">
          <Button variant="outline" onClick={onSkip}>
            Skip
          </Button>
          <Button variant="primary" onClick={handleSelect} disabled={!selected}>
            Continue
          </Button>
        </div>
      </div>
    </Modal>
  );
};
