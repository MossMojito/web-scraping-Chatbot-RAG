import { Dumbbell } from "lucide-react";

const ChatHeader = () => {
  return (
    <header className="gradient-header px-4 py-5 shadow-soft">
      <div className="max-w-2xl mx-auto flex items-center justify-center gap-3">
        <div className="bg-primary-foreground/20 p-2 rounded-full">
          <Dumbbell className="w-6 h-6 text-primary-foreground" />
        </div>
        <h1 className="text-xl md:text-2xl font-semibold text-primary-foreground tracking-wide">
          ค้นหาสถานที่ออกกำลังกาย
        </h1>
      </div>
    </header>
  );
};

export default ChatHeader;
