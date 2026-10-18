"use client";
import { useEffect, useRef, useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { CATEGORIES, LEVELS } from "@/lib/types";

const field = "rounded border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-steel-600 focus:outline-none focus:ring-2 focus:ring-steel-100";

export default function FilterBar() {
  const router = useRouter();
  const pathname = usePathname();
  const sp = useSearchParams();
  const [q, setQ] = useState(sp.get("q") ?? "");
  const first = useRef(true);

  function set(key: string, value: string) {
    const p = new URLSearchParams(sp.toString());
    if (value) p.set(key, value); else p.delete(key);
    router.replace(`${pathname}?${p.toString()}`, { scroll: false });
  }

  // Arama kutusu: yazmayı bıraktıktan 300 ms sonra filtrele
  useEffect(() => {
    if (first.current) { first.current = false; return; }
    const t = setTimeout(() => set("q", q.trim()), 300);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q]);

  const durum = sp.get("durum") ?? "aktif";

  return (
    <div className="space-y-4">
      <div role="tablist" aria-label="Başvuru durumu" className="inline-flex rounded border border-slate-300 bg-white p-0.5">
        {[["aktif", "Aktif başvurular"], ["gecmis", "Süresi dolanlar"]].map(([v, label]) => (
          <button
            key={v} role="tab" aria-selected={durum === v}
            onClick={() => set("durum", v === "aktif" ? "" : v)}
            className={`rounded px-4 py-2 text-sm font-medium ${durum === v ? "bg-navy-800 text-white" : "text-slate-700 hover:bg-slate-50"}`}
          >{label}</button>
        ))}
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <input
          type="search" value={q} onChange={(e) => setQ(e.target.value)}
          placeholder="Etkinlik veya kurum ara" aria-label="Etkinlik veya kurum ara"
          className={`${field} sm:col-span-2 lg:col-span-1`}
        />
        <select aria-label="Kategori" value={sp.get("kategori") ?? ""} onChange={(e) => set("kategori", e.target.value)} className={field}>
          <option value="">Tüm kategoriler</option>
          {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
        <select aria-label="Seviye" value={sp.get("seviye") ?? ""} onChange={(e) => set("seviye", e.target.value)} className={field}>
          <option value="">Tüm seviyeler</option>
          {LEVELS.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
        </select>
        <select aria-label="Sıralama" value={sp.get("sirala") ?? ""} onChange={(e) => set("sirala", e.target.value)} className={field}>
          <option value="">Son başvuru tarihi en yakın</option>
          <option value="yeni">En yeni eklenenler</option>
        </select>
      </div>
    </div>
  );
}
