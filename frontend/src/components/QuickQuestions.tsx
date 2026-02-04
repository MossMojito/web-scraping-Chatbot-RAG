import { Button } from "@/components/ui/button";

interface QuickQuestionsProps {
  onSelect: (question: string) => void;
  disabled?: boolean;
}

const questions = [
  "หาโยคะในกรุงเทพ",
  "มีอะไรบ้าง",
  "มวยไทยดีอย่างไร",
];

const QuickQuestions = ({ onSelect, disabled }: QuickQuestionsProps) => {
  return (
    <div className="flex flex-wrap gap-2 justify-center px-4 py-3 bg-muted/50 border-t border-border">
      <span className="w-full text-center text-xs text-muted-foreground mb-1">
        คำถามยอดนิยม
      </span>
      {questions.map((question) => (
        <Button
          key={question}
          variant="quickQuestion"
          size="sm"
          onClick={() => onSelect(question)}
          disabled={disabled}
          className="text-xs md:text-sm"
        >
          {question}
        </Button>
      ))}
    </div>
  );
};

export default QuickQuestions;
