/*
  # Create Restaurant Table

  1. New Tables
    - `restaurant`
      - `id` (uuid, primary key) - Unique identifier for each restaurant
      - `id_unique` (text, unique) - Unique identifier based on name and city
      - `nom` (text) - Restaurant name
      - `note` (float) - Average rating (1-5)
      - `nb_avis` (int) - Number of reviews
      - `ville` (text) - City name
      - `pays` (text) - Country name
      - `pop_city` (text) - City population
      - `all_pop_city` (text) - City + periphery population
      - `created_at` (timestamptz) - Creation timestamp
      - `updated_at` (timestamptz) - Last update timestamp

  2. Security
    - Enable RLS on `restaurant` table
    - Add policy for public read access (data is public)

  3. Indexes
    - Index on `ville` for faster queries by city
    - Index on `id_unique` for faster lookups
*/

CREATE TABLE IF NOT EXISTS restaurant (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  id_unique text UNIQUE NOT NULL,
  nom text NOT NULL,
  note float NOT NULL,
  nb_avis int NOT NULL,
  ville text NOT NULL,
  pays text NOT NULL DEFAULT 'Inconnu',
  pop_city text NOT NULL DEFAULT '0',
  all_pop_city text NOT NULL DEFAULT '0',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE restaurant ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to restaurants"
  ON restaurant
  FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Allow public insert for restaurants"
  ON restaurant
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Allow public update for restaurants"
  ON restaurant
  FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_restaurant_ville ON restaurant(ville);
CREATE INDEX IF NOT EXISTS idx_restaurant_id_unique ON restaurant(id_unique);