import React from 'react';

const KeywordBubble = ({ text, category = 'general', onClick }) => {
  const getCategoryColor = () => {
    const colors = {
      urgency: 'bg-[#FB7185]/20 text-[#FB7185] border-[#FB7185]/30',
      location: 'bg-[#6D28D9]/20 text-[#6D28D9] border-[#6D28D9]/30',
      damage: 'bg-[#F59E0B]/20 text-[#F59E0B] border-[#F59E0B]/30',
      vehicle: 'bg-[#3B82F6]/20 text-[#3B82F6] border-[#3B82F6]/30',
      success: 'bg-[#34D399]/20 text-[#34D399] border-[#34D399]/30',
      general: 'bg-[#374151]/20 text-[#374151] border-[#374151]/30'
    };
    return colors[category] || colors.general;
  };

  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-full border ${getCategoryColor()} transition-all duration-300 hover:scale-105 active:scale-95 float-animation`}
      style={{ animationDelay: `${Math.random() * 2}s` }}
    >
      <span className="font-medium">{text}</span>
    </button>
  );
};

export default KeywordBubble;