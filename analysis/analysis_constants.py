# analysis_constants.py 


supply_centers = [
    "ANK", "ARM", "BEL", "BER", "BUD", "BUL", "CON", "DEN", "EDI", "GRE",
    "HOL", "KIE", "LON", "LVP", "MAR", "MOS", "MUN", "NAP", "PAR", "POR",
    "ROM", "RUM", "SER", "SEV", "SMY", "SWE", "TRI", "TUN",
    "VEN", "VIE", "WAR", 
    "SPA", "STP", "BUL" # coastal provinces
]

coastal_scs = ["SPA/SC", "SPA/NC",
    "STP/SC", "STP/NC", 'BUL/EC',
       'BUL/SC',]

COUNTRIES = ['AUSTRIA', 'ENGLAND', 'FRANCE', 'GERMANY', 'ITALY', 'RUSSIA', 'TURKEY']

place_identifier = "[A-Z]{3}(?:/[A-Z]{2})?"
place_capturing_regex = r"([A-Z]{3})"
unit_identifier = rf"[AF] {place_identifier}"
unit_move = rf"{unit_identifier} . {place_identifier}"

possible_commands = {
    "Move": f"^"+unit_move, # distinguishing this from support
    "Support Move": f"{unit_identifier} S {unit_move}",
    "Support Hold": fr"{unit_identifier} S {unit_identifier}(?!\s+[.\-]\s+{place_identifier})",
    "Convoy": f"F {place_identifier} C {unit_move}", # No convoys in here? 
    "Hold": f"{unit_identifier} H",
    "Build": f"{unit_identifier} B",
    "Disband": f"{unit_identifier} D",
    "Retreat": f"{unit_identifier} R",
}