export type Category = "staj" | "hackathon" | "yarisma" | "bootcamp" | "konferans";
export type Level = "lise" | "lisans" | "yuksek-lisans";

export interface EventRow {
  id: string;
  slug: string;
  title: string;
  organization: string;
  description: string | null;
  category: Category;
  education_levels: Level[];
  application_url: string;
  image_url: string | null;
  deadline: string | null;
  is_online: boolean | null;
  location: string | null;
  created_at: string;
}

export const CATEGORIES: { value: Category; label: string }[] = [
  { value: "staj", label: "Staj" },
  { value: "hackathon", label: "Hackathon" },
  { value: "yarisma", label: "Yarışma" },
  { value: "bootcamp", label: "Boot-camp" },
  { value: "konferans", label: "Konferans / Webinar" },
];
export const LEVELS: { value: Level; label: string }[] = [
  { value: "lise", label: "Lise" },
  { value: "lisans", label: "Lisans" },
  { value: "yuksek-lisans", label: "Yüksek Lisans" },
];
export const categoryLabel = (c: string) => CATEGORIES.find((x) => x.value === c)?.label ?? c;
export const levelLabel = (l: string) => LEVELS.find((x) => x.value === l)?.label ?? l;
