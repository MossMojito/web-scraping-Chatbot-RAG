const BotAvatar = () => {
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="w-10 h-10 rounded-full gradient-header shadow-soft flex items-center justify-center text-primary-foreground text-lg font-semibold">
        🏃‍♀️
      </div>
      <span className="text-xs text-muted-foreground font-medium">น้องฟิต</span>
    </div>
  );
};

export default BotAvatar;
