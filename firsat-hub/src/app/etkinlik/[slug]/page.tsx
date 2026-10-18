import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getEvent } from "@/lib/events";
import { categoryLabel, levelLabel } from "@/lib/types";
import { daysLeft, formatDate } from "@/lib/calendar";
import DeadlineBadge from "@/components/DeadlineBadge";
import CalendarButtons from "@/components/CalendarButtons";
import { Logo } from "@/components/EventCard";

export const revalidate = 300;

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const e = await getEvent((await params).slug);
  return e ? { title: e.title, description: (e.description ?? "").slice(0, 160) } : {};
}

export default async function EventPage({ params }: { params: Promise<{ slug: string }> }) {
  const event = await getEvent((await params).slug);
  if (!event) notFound();
  const closed = (daysLeft(event.deadline) ?? 0) < 0;

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <Link href="/" className="text-sm text-steel-600 hover:underline">Tüm etkinlikler</Link>

      <div className="rounded-lg border border-slate-200 bg-white p-6 sm:p-8">
        <div className="flex items-start gap-4">
          <Logo event={event} size={72} />
          <div>
            <h1 className="text-2xl font-semibold leading-snug text-navy-900">{event.title}</h1>
            <p className="mt-1 text-slate-600">{event.organization}</p>
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-1.5">
          <span className="rounded bg-navy-800 px-2 py-0.5 text-xs font-medium text-white">{categoryLabel(event.category)}</span>
          {event.education_levels.map((l) => (
            <span key={l} className="rounded border border-slate-300 px-2 py-0.5 text-xs text-slate-700">{levelLabel(l)}</span>
          ))}
        </div>

        <dl className="mt-6 grid gap-4 border-y border-slate-100 py-5 sm:grid-cols-3">
          <div><dt className="text-sm text-slate-500">Son başvuru</dt><dd className="mt-1 font-medium">{formatDate(event.deadline)}</dd></div>
          <div><dt className="text-sm text-slate-500">Durum</dt><dd className="mt-1"><DeadlineBadge deadline={event.deadline} /></dd></div>
          <div><dt className="text-sm text-slate-500">Yer</dt><dd className="mt-1 font-medium">{event.is_online ? "Çevrimiçi" : event.location ?? "Belirtilmemiş"}</dd></div>
        </dl>

        {event.description && <p className="mt-6 max-w-prose whitespace-pre-line leading-relaxed text-slate-700">{event.description}</p>}

        {!closed && (
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <a href={event.application_url} target="_blank" rel="noopener noreferrer" className="rounded bg-navy-800 px-5 py-2.5 font-medium text-white hover:bg-navy-700">Başvur</a>
            <CalendarButtons event={event} />
          </div>
        )}
      </div>
    </div>
  );
}
