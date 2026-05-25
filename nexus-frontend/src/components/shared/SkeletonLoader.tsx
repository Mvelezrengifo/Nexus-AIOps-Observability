export const SkeletonLoader = ({ count = 1, className = 'h-4 bg-gray-700 rounded' }) => (
  <div className="space-y-2">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className={`animate-pulse ${className}`} />
    ))}
  </div>
);