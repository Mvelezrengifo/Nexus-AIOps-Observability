export const LoadingSpinner = ({ fullscreen = false, label = 'Loading...' }) => {
  const spinner = (
    <div className="flex flex-col items-center gap-2">
      <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      <p className="text-gray-400 text-sm">{label}</p>
    </div>
  );
  if (fullscreen) {
    return (
      <div className="fixed inset-0 bg-gray-950/80 flex items-center justify-center z-50">
        {spinner}
      </div>
    );
  }
  return spinner;
};