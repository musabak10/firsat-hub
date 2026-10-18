import { getEvent } from "@/lib/events";
import { buildIcs } from "@/lib/calendar";

export async function GET(_: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const event = await getEvent(slug);
  const ics = event ? buildIcs(event) : null;
  if (!ics) return new Response("Bulunamadı", { status: 404 });
  return new Response(ics, {
    headers: {
      "Content-Type": "text/calendar; charset=utf-8",
      "Content-Disposition": `attachment; filename="${slug}.ics"`,
    },
  });
}
