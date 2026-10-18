"""Deterministically assign lower player IDs to larger tee-position counts."""
def rank_entry(entry):
    groups = {int(p): slots for p, slots in entry['groups'].items()}
    order = sorted(groups, key=lambda p: (-len(set(groups[p])), p))
    mapping = {old: new for new, old in enumerate(order, 1)}
    return {**entry,
            'rounds': [[sorted(mapping[p] for p in group) for group in rd]
                       for rd in entry['rounds']],
            'groups': {mapping[p]: groups[p] for p in order},
            'grid': [[mapping[p] if p is not None else None for p in row]
                     for row in entry['grid']]}, mapping
