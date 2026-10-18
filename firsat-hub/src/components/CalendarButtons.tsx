"use client";
import { useState } from "react";
import { googleCalendarUrl } from "@/lib/calendar";
import type { EventRow } from "@/lib/types";

export default function CalendarButtons({ event, compact = false }: { event: EventRow; compact?: boolean }) {
  const [open, setOpen] = useState(false);
  const google = googleCalendarUrl(event);
  if (!google) return null;

  const base = "rounded border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-navy-800 hover:bg-slate-50";

  if (!compact) {
    return (
      <div className="flex flex-wrap gap-2">
        <a href={google} target="_blank" rel="noopener noreferrer" className={base}>Google Takvim&apos;e ekle</a>
        <a href={`/api/ics/${event.slug}`} className={base}>.ics indir</a>
      </div>
    );
  }
  return (
    <div className="relative">
      <button type="button" onClick={() => setOpen((o) => !o)} aria-expanded={open} className={base}>
        Hatırlatıcı ekle
      </button>
      {open && (
        <div className="absolute bottom-full right-0 z-10 mb-1 w-44 rounded border border-slate-200 bg-white p-1 shadow-lg">
          <a href={google} target="_blank" rel="noopener noreferrer" className="block rounded px-3 py-2 text-sm hover:bg-slate-50">Google Takvim</a>
          <a href={`/api/ics/${event.slug}`} className="block rounded px-3 py-2 text-sm hover:bg-slate-50">.ics dosyası</a>
        </div>
      )}
    </div>
  );
}
