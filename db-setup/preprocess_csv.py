#!/usr/bin/env python3
"""
Preprocess FM2017 CSV to match database schema
Converts CSV column names from camelCase to snake_case matching database columns
"""

import csv
from pathlib import Path


# Column mapping from CSV to Database
COLUMN_MAPPING = {
    'UID': None,  # Skip - database has auto-increment player_id
    'Name': 'name',
    'NationID': 'nation_extid',
    'Born': 'born',
    'Age': 'age',
    'IntCaps': 'int_caps',
    'IntGoals': 'int_goals',
    'U21Caps': 'u21_caps',
    'U21Goals': 'u21_goals',
    'Height': 'height',
    'Weight': 'weight',
    'AerialAbility': 'aerial_ability',
    'CommandOfArea': 'command_of_area',
    'Communication': 'communication',
    'Eccentricity': 'eccentricity',
    'Handling': 'handling',
    'Kicking': 'kicking',
    'OneOnOnes': 'one_on_ones',
    'Reflexes': 'reflexes',
    'RushingOut': 'rushing_out',
    'TendencyToPunch': 'tendency_to_punch',
    'Throwing': 'throwing',
    'Corners': 'corners',
    'Crossing': 'crossing',
    'Dribbling': 'dribbling',
    'Finishing': 'finishing',
    'FirstTouch': 'first_touch',
    'Freekicks': 'free_kicks',
    'Heading': 'heading',
    'LongShots': 'long_shots',
    'Longthrows': 'long_throws',
    'Marking': 'marking',
    'Passing': 'passing',
    'PenaltyTaking': 'penalty_taking',
    'Tackling': 'tackling',
    'Technique': 'technique',
    'Aggression': 'aggression',
    'Anticipation': 'anticipation',
    'Bravery': 'bravery',
    'Composure': 'composure',
    'Concentration': 'concentration',
    'Vision': 'vision',
    'Decisions': 'decisions',
    'Determination': 'determination',
    'Flair': 'flair',
    'Leadership': 'leadership',
    'OffTheBall': 'off_the_ball',
    'Positioning': 'positioning',
    'Teamwork': 'teamwork',
    'Workrate': 'work_rate',
    'Acceleration': 'acceleration',
    'Agility': 'agility',
    'Balance': 'balance',
    'Jumping': 'jumping',
    'LeftFoot': 'left_foot',
    'NaturalFitness': 'natural_fitness',
    'Pace': 'pace',
    'RightFoot': 'right_foot',
    'Stamina': 'stamina',
    'Strength': 'strength',
    'Consistency': 'consistency',
    'Dirtiness': 'dirtiness',
    'ImportantMatches': 'important_matches',
    'InjuryProness': 'injury_proness',
    'Versatility': 'versatility',
    'Adaptability': 'adaptability',
    'Ambition': 'ambition',
    'Loyalty': 'loyalty',
    'Pressure': 'pressure',
    'Professional': 'professional',
    'Sportsmanship': 'sportsmanship',
    'Temperament': 'temperament',
    'Controversy': 'controversy',
    'PositionsDesc': None,  # Skip - not in database
    'Goalkeeper': 'goalkeeper',
    'Sweeper': 'sweeper',
    'Striker': 'striker',
    'AttackingMidCentral': 'attacking_mid_central',
    'AttackingMidLeft': 'attacking_mid_left',
    'AttackingMidRight': 'attacking_mid_right',
    'DefenderCentral': 'defender_central',
    'DefenderLeft': 'defender_left',
    'DefenderRight': 'defender_right',
    'DefensiveMidfielder': 'defensive_midfielder',
    'MidfielderCentral': 'midfield_central',
    'MidfielderLeft': 'midfield_left',
    'MidfielderRight': 'midfield_right',
    'WingBackLeft': 'wingback_left',
    'WingBackRight': 'wingback_right'
}


def preprocess_csv(input_path: str, output_path: str):
    """
    Preprocess CSV file to match database schema
    
    Args:
        input_path: Path to original CSV
        output_path: Path to save processed CSV
    """
    print("="*60)
    print("CSV Preprocessing for FM2017 Dataset")
    print("="*60)
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print("="*60 + "\n")
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Map headers to database column names
        db_headers = []
        csv_to_db_map = {}
        
        # Get fieldnames (guaranteed to exist after reading CSV)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            raise ValueError("CSV file has no headers")
        
        for csv_col in fieldnames:
            db_col = COLUMN_MAPPING.get(csv_col)
            if db_col is not None:  # Only include mapped columns
                db_headers.append(db_col)
                csv_to_db_map[csv_col] = db_col
        
        print(f"✓ Mapped {len(db_headers)} columns")
        print(f"✗ Skipped {len(fieldnames) - len(db_headers)} columns\n")
        
        # Write processed CSV
        with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=db_headers)
            writer.writeheader()
            
            row_count = 0
            for row in reader:
                # Map row data to database column names
                db_row = {}
                for csv_col, db_col in csv_to_db_map.items():
                    db_row[db_col] = row[csv_col]
                
                writer.writerow(db_row)
                row_count += 1
                
                if row_count % 10000 == 0:
                    print(f"  Processed {row_count} rows...")
            
            print(f"\n✓ Processed {row_count} total rows")
    
    print(f"✓ Saved to: {output_path}")
    print("="*60 + "\n")


def main():
    """Main function"""
    script_dir = Path(__file__).parent
    input_csv = script_dir.parent / "fman_initial_Dat_Analysis_test" / "fbmandataset.csv"
    output_csv = script_dir.parent / "fman_initial_Dat_Analysis_test" / "fbmandataset_processed.csv"
    
    if not input_csv.exists():
        print(f"ERROR: Input CSV not found: {input_csv}")
        return 1
    
    preprocess_csv(str(input_csv), str(output_csv))
    
    print("✓ CSV preprocessing complete!")
    print(f"✓ You can now import: {output_csv}")
    
    return 0


if __name__ == "__main__":
    exit(main())
