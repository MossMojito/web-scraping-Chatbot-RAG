import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const ChatInput = ({ onSend, disabled }: ChatInputProps) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-2 p-4 bg-card border-t border-border shadow-card"
    >
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="พิมพ์ข้อความของคุณ..."
        disabled={disabled}
        className="flex-1 bg-muted/50 border-border focus-visible:ring-primary"
      />
      <Button
        type="submit"
        disabled={disabled || !input.trim()}
        variant="send"
        size="icon"
        className="shrink-0"
      >
        <Send className="w-5 h-5" />
        <span className="sr-only">ส่ง</span>
      </Button>
    </form>
  );
};

export default ChatInput;
