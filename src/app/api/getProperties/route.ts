// route.ts
import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.VACANT_LOTS_DB,
});

export const POST = async (req: NextRequest) => {
  const body = await req.json();
  const { xmin, ymin, xmax, ymax } = body;

  const query = `
    SELECT * FROM vacant_properties_end
    WHERE ST_Within(geometry, ST_MakeEnvelope($1, $2, $3, $4, 2272));
  `;

  try {
    const result = await pool.query(query, [xmin, ymin, xmax, ymax]);
    return NextResponse.json(result.rows, { status: 200 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};