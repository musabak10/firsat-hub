import { daysLeft } from "@/lib/calendar";

export default function DeadlineBadge({ deadline }: { deadline: string | null }) {
  const d = daysLeft(deadline);
  if (d === null) return <span className="rounded bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">Sürekli başvuru</span>;
  if (d < 0) return <span className="rounded bg-slate-200 px-2 py-1 text-xs font-medium text-slate-600">Başvuru kapandı</span>;
  if (d === 0) return <span className="rounded bg-red-600 px-2 py-1 text-xs font-semibold text-white">Son gün bugün!</span>;
  if (d <= 3) return <span className="rounded bg-red-600 px-2 py-1 text-xs font-semibold text-white">Başvuru için son {d} gün!</span>;
  if (d <= 7) return <span className="rounded bg-orange-500 px-2 py-1 text-xs font-semibold text-white">Son {d} gün</span>;
  return <span className="rounded bg-steel-100 px-2 py-1 text-xs font-medium text-navy-800">{d} gün kaldı</span>;
}
