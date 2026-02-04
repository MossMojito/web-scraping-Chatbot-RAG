import { cn } from "@/lib/utils";
import BotAvatar from "./BotAvatar";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  isTyping?: boolean;
}

const ChatMessage = ({ message, isUser, isTyping }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex gap-3 animate-slide-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {!isUser && <BotAvatar />}
      
      <div
        className={cn(
          "max-w-[75%] md:max-w-[65%] px-4 py-3 shadow-card",
          isUser
            ? "bg-user-bubble text-user-foreground rounded-bubble rounded-br-md"
            : "bg-bot-bubble text-bot-foreground rounded-bubble rounded-bl-md"
        )}
      >
        {isTyping ? (
          <div className="flex gap-1.5 py-1">
            <span className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-pulse-soft" style={{ animationDelay: "0ms" }} />
            <span className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-pulse-soft" style={{ animationDelay: "150ms" }} />
            <span className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-pulse-soft" style={{ animationDelay: "300ms" }} />
          </div>
        ) : (
          <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{message}</p>
        )}
      </div>
      
      {isUser && (
        <div className="w-10 h-10 rounded-full bg-secondary shadow-soft flex items-center justify-center text-secondary-foreground text-lg">
          👤
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
