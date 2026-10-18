import { supabase } from "./supabase";
import type { EventRow } from "./types";

export interface Filters {
  kategori?: string;
  seviye?: string;
  durum?: string; // "aktif" (varsayılan) | "gecmis"
  q?: string;
  sirala?: string; // "deadline" (varsayılan) | "yeni"
}

export async function getEvents(f: Filters): Promise<EventRow[]> {
  const nowIso = new Date().toISOString();
  let query = supabase().from("events").select("*").eq("status", "approved");

  if (f.durum === "gecmis") query = query.lt("deadline", nowIso);
  else query = query.or(`deadline.gte.${nowIso},deadline.is.null`);

  if (f.kategori) query = query.eq("category", f.kategori);
  if (f.seviye) query = query.contains("education_levels", [f.seviye]);
  if (f.q) {
    const s = f.q.replace(/[%,()]/g, " ").trim();
    if (s) query = query.or(`title.ilike.%${s}%,organization.ilike.%${s}%`);
  }

  if (f.sirala === "yeni") query = query.order("created_at", { ascending: false });
  else if (f.durum === "gecmis") query = query.order("deadline", { ascending: false });
  else query = query.order("deadline", { ascending: true, nullsFirst: false });

  const { data, error } = await query.limit(60);
  if (error) throw new Error(error.message);
  return (data ?? []) as EventRow[];
}

export async function getEvent(slug: string): Promise<EventRow | null> {
  const { data } = await supabase().from("events").select("*").eq("slug", slug).eq("status", "approved").maybeSingle();
  return (data as EventRow) ?? null;
}
