import { useState, useRef, useEffect } from "react";
import { toast } from "sonner";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import QuickQuestions from "./QuickQuestions";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
}

const WELCOME_MESSAGE =
  "สวัสดีค่ะ! ฉันชื่อน้องฟิต 🏃‍♀️ ยินดีช่วยค้นหาสถานที่ออกกำลังกายที่เหมาะกับคุณค่ะ คุณสนใจกิจกรรมประเภทไหนคะ?";

const ChatContainer = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: "welcome", text: WELCOME_MESSAGE, isUser: false },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (userMessage: string) => {
    const userMsgId = Date.now().toString();
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, text: userMessage, isUser: true },
    ]);
    setIsLoading(true);

    try {
      const response = await fetch(
        "https://yellowpages-chatbot-api.onrender.com/chat",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userMessage }),
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      const botMsgId = (Date.now() + 1).toString();

      setMessages((prev) => [
        ...prev,
        { id: botMsgId, text: data.response, isUser: false },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้ กรุณาลองใหม่อีกครั้ง", {
        description:
          "เซิร์ฟเวอร์มีปัญหาในการประมวลผลคำขอ (เช่น API key ไม่ถูกต้อง) กรุณาลองใหม่ภายหลัง",
      });

      // Add fallback response
      const fallbackMsgId = (Date.now() + 1).toString();
      setMessages((prev) => [
        ...prev,
        {
          id: fallbackMsgId,
          text: "ขออภัยค่ะ เซิร์ฟเวอร์มีปัญหาในการตอบกลับตอนนี้ กรุณาลองใหม่อีกครั้งนะคะ 🙏",
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <ChatHeader />

      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg.text} isUser={msg.isUser} />
          ))}

          {isLoading && (
            <ChatMessage message="" isUser={false} isTyping />
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      <div className="sticky bottom-0 bg-card">
        <QuickQuestions onSelect={sendMessage} disabled={isLoading} />
        <ChatInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatContainer;
