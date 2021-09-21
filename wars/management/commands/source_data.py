import csv
from pathlib import Path

from django.core.management import BaseCommand

from wars.models import Battle, BattleType, Region, Location, Warrior


class Command(BaseCommand):
    """
        Created Records  from csv file to Table

        python manage.py source_data --file_path=<file_path>
    """

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        if file_path:
            if not Path(file_path).is_file():
                self.stdout.write(self.style.ERROR(f"file does not exists"))
        else:
            self.stdout.write(self.style.ERROR(f"add param --file_path=<file_path>'"))
        create_record_obj = CreateRecord(file_path)
        total_record_added = create_record_obj.create_records()
        print("total crated records: ", total_record_added)


class CreateRecord:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_records(self):
        rows = self.get_rows()
        count = 0
        for row in rows:
            location_obj = self.get_location_object(row)
            attacker_outcome = None
            if row['attacker_outcome'] == 'win':
                attacker_outcome = True
            elif row['attacker_outcome'] == 'loss':
                attacker_outcome = False
            obj = Battle(
                title=row['name'],
                year=row['year'],
                battle_number=row['battle_number'],
                attacker_king=self.get_warrior(row['attacker_king'], True),
                defender_king=self.get_warrior(row['defender_king'], True),
                is_attacker_win=attacker_outcome,
                battle_type=self.get_battle_type(row),
                death=row['major_death'] if row['major_death'] else None,
                capture=row['major_capture'] if row['major_capture'] else None,
                attacker_size=row['attacker_size'] if row['attacker_size'] else None,
                defender_size=row['defender_size'] if row['defender_size'] else None,
                is_summer=row['summer'] if row['summer'] else None,
                location=location_obj,
                note=row['note']
            )
            obj.save()
            attackers = [self.get_warrior(row[f'attacker_{i}']) for i in range(1, 5)]
            obj.attackers.add(*attackers)
            defenders = [self.get_warrior(row[f'defender_{i}']) for i in range(1, 5)]
            obj.defenders.add(*defenders)
            attacker_commanders = [self.get_warrior(name.strip(' ')) for name in row['attacker_commander'].split(',') if
                                   name]
            obj.attacker_commanders.add(*attacker_commanders)
            defender_commanders = [self.get_warrior(name.strip(' ')) for name in row['defender_commander'].split(',') if
                                   name]
            obj.defender_commanders.add(*defender_commanders)
            count += 1
        return count

    def get_rows(self):
        with open(self.file_path, 'r') as csv_file:
            rows = csv.DictReader(csv_file)
            rows = [row for row in rows]
            return rows

    def get_location_object(self, row):
        region = row.get('region')
        location = row.get('location')
        region_obj = Region.objects.get(title=region)
        location_obj, created = Location.objects.get_or_create(title=location, region=region_obj)
        return location_obj

    def get_warrior(self, name, is_king=None):
        obj, created = Warrior.objects.get_or_create(name=name)
        if created and is_king:
            obj.is_king = True
        return obj

    def get_battle_type(self, row):
        title = row['battle_type']
        obj, created = BattleType.objects.get_or_create(title=title)
        return obj
