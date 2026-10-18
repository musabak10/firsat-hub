import Link from "next/link";
import type { EventRow } from "@/lib/types";
import { categoryLabel, levelLabel } from "@/lib/types";
import { daysLeft, formatDate } from "@/lib/calendar";
import DeadlineBadge from "./DeadlineBadge";
import CalendarButtons from "./CalendarButtons";

export function Logo({ event, size = 56 }: { event: EventRow; size?: number }) {
  const s = { width: size, height: size };
  return event.image_url ? (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={event.image_url} alt="" style={s} className="shrink-0 rounded border border-slate-200 bg-white object-contain" />
  ) : (
    <div style={s} className="flex shrink-0 items-center justify-center rounded bg-navy-800 text-lg font-semibold text-white" aria-hidden>
      {event.organization.charAt(0).toUpperCase()}
    </div>
  );
}

export default function EventCard({ event }: { event: EventRow }) {
  const closed = (daysLeft(event.deadline) ?? 0) < 0;
  return (
    <article className="flex flex-col rounded-lg border border-slate-200 bg-white p-5">
      <div className="flex items-start gap-4">
        <Logo event={event} />
        <div className="min-w-0 flex-1">
          <h2 className="text-base font-semibold leading-snug text-navy-900">
            <Link href={`/etkinlik/${event.slug}`} className="hover:underline">{event.title}</Link>
          </h2>
          <p className="mt-0.5 text-sm text-slate-600">{event.organization}</p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-1.5">
        <span className="rounded bg-navy-800 px-2 py-0.5 text-xs font-medium text-white">{categoryLabel(event.category)}</span>
        {event.education_levels.map((l) => (
          <span key={l} className="rounded border border-slate-300 px-2 py-0.5 text-xs text-slate-700">{levelLabel(l)}</span>
        ))}
        {event.is_online && <span className="rounded border border-slate-300 px-2 py-0.5 text-xs text-slate-700">Çevrimiçi</span>}
      </div>

      <div className="mt-4 flex items-center justify-between gap-2">
        <DeadlineBadge deadline={event.deadline} />
        <span className="text-xs text-slate-500">{formatDate(event.deadline)}</span>
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-2 border-t border-slate-100 pt-4">
        <Link href={`/etkinlik/${event.slug}`} className="rounded border border-slate-300 px-3 py-2 text-sm font-medium text-navy-800 hover:bg-slate-50">Detayları gör</Link>
        {!closed && (
          <a href={event.application_url} target="_blank" rel="noopener noreferrer" className="rounded bg-navy-800 px-3 py-2 text-sm font-medium text-white hover:bg-navy-700">Başvur</a>
        )}
        {!closed && <div className="ml-auto"><CalendarButtons event={event} compact /></div>}
      </div>
    </article>
  );
}
