import React from 'react';

const RiskHeatmap = () => {
  const hours = Array.from({ length: 24 }, (_, i) => i);
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  
  const generateHeatmapData = () => {
    const data = [];
    for (let day = 0; day < 7; day++) {
      for (let hour = 0; hour < 24; hour++) {
        // Generate random risk scores
        const baseRisk = Math.floor(Math.random() * 100);
        // Higher risk during business hours
        const hourAdjustment = hour >= 8 && hour <= 18 ? 20 : -10;
        // Higher risk on weekdays
        const dayAdjustment = day < 5 ? 15 : -15;
        
        let risk = Math.max(0, Math.min(100, baseRisk + hourAdjustment + dayAdjustment));
        
        // Add some patterns
        if (day === 2 && hour === 14) risk = 85; // Wednesday afternoon peak
        if (day === 5 && hour === 10) risk = 90; // Saturday morning peak
        if (day === 0 && hour === 4) risk = 10; // Sunday early morning low
        
        data.push({ day, hour, risk });
      }
    }
    return data;
  };

  const heatmapData = generateHeatmapData();

  const getRiskColor = (risk) => {
    if (risk < 30) return 'bg-[#34D399]/20';
    if (risk < 50) return 'bg-[#34D399]/40';
    if (risk < 60) return 'bg-[#F59E0B]/40';
    if (risk < 70) return 'bg-[#F59E0B]/60';
    if (risk < 80) return 'bg-[#FB7185]/50';
    return 'bg-[#FB7185]/70';
  };

  return (
    <div className="overflow-x-auto">
      <div className="min-w-max">
        <div className="flex items-start">
          {/* Time labels */}
          <div className="w-12 pt-8">
            <div className="h-8"></div>
            {hours.map(hour => (
              <div key={hour} className="h-6 text-xs text-[#374151] flex items-center justify-end pr-2">
                {hour}:00
              </div>
            ))}
          </div>

          {/* Heatmap grid */}
          <div>
            {/* Day labels */}
            <div className="flex mb-2">
              {days.map(day => (
                <div key={day} className="w-6 text-center text-sm font-medium text-[#374151]">
                  {day}
                </div>
              ))}
            </div>

            {/* Heatmap cells */}
            <div className="flex">
              {days.map((_, dayIndex) => (
                <div key={dayIndex} className="flex flex-col">
                  {hours.map(hour => {
                    const dataPoint = heatmapData.find(d => d.day === dayIndex && d.hour === hour);
                    return (
                      <div
                        key={`${dayIndex}-${hour}`}
                        className={`w-6 h-6 border border-white ${getRiskColor(dataPoint?.risk || 0)} 
                          hover:scale-125 hover:z-10 hover:shadow-lg transition-transform cursor-pointer`}
                        title={`Risk: ${dataPoint?.risk || 0}/100`}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center mt-6 space-x-4">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-[#34D399]/20 mr-2"></div>
            <span className="text-xs text-[#374151]">Low (0-30)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-[#34D399]/40 mr-2"></div>
            <span className="text-xs text-[#374151]">Medium-Low</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-[#F59E0B]/40 mr-2"></div>
            <span className="text-xs text-[#374151]">Medium</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-[#F59E0B]/60 mr-2"></div>
            <span className="text-xs text-[#374151]">Medium-High</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-[#FB7185]/50 mr-2"></div>
            <span className="text-xs text-[#374151]">High (80-100)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskHeatmap;