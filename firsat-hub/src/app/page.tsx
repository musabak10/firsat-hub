import { Suspense } from "react";
import { getEvents, type Filters } from "@/lib/events";
import EventCard from "@/components/EventCard";
import FilterBar from "@/components/FilterBar";

export const revalidate = 300;

export default async function Home({ searchParams }: { searchParams: Promise<Filters> }) {
  const filters = await searchParams;
  const events = await getEvents(filters);

  return (
    <div className="space-y-8">
      <section>
        <h1 className="max-w-2xl text-3xl font-semibold leading-tight text-navy-900">
          Öğrenciler için staj, hackathon ve yarışmalar
        </h1>
        <p className="mt-2 max-w-xl text-slate-600">Başvuru tarihi yaklaşanlar önce gelir. Hatırlatıcıyı takvimine tek tıkla ekle.</p>
      </section>

      <Suspense><FilterBar /></Suspense>

      <p className="text-sm text-slate-500" aria-live="polite">{events.length} etkinlik</p>

      {events.length === 0 ? (
        <div className="rounded-lg border border-dashed border-slate-300 bg-white p-10 text-center text-slate-600">
          Bu filtrelerle etkinlik bulunamadı. Filtreleri değiştirmeyi veya aramayı kısaltmayı dene.
        </div>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {events.map((e) => <EventCard key={e.id} event={e} />)}
        </div>
      )}
    </div>
  );
}
