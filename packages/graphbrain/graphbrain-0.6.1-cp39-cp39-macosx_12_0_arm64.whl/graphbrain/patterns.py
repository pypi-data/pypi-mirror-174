from collections import Counter
from graphbrain import hedge
from graphbrain.hyperedge import edge_matches_pattern


def edge2pattern(edge, root=False, subtype=False):
    if root and edge.atom:
        root_str = edge.root()
    else:
        root_str = '*'
    if subtype:
        et = edge.type()
    else:
        et = edge.mtype()
    pattern = '{}/{}'.format(root_str, et)
    ar = edge.argroles()
    if ar == '':
        return hedge(pattern)
    else:
        return hedge('{}.{}'.format(pattern, ar))


def inner_edge_matches_pattern(edge, pattern):
    if edge.atom:
        return False
    for subedge in edge:
        if edge_matches_pattern(subedge, pattern):
            return True
    for subedge in edge:
        if inner_edge_matches_pattern(subedge, pattern):
            return True
    return False


class PatternCounter:
    def __init__(self,
                 depth=2,
                 count_subedges=True,
                 expansions={'*'},
                 match_roots=set(),
                 match_subtypes=set()):
        self.patterns = Counter()
        self.depth = depth
        self.count_subedges = count_subedges
        self.expansions = expansions
        self.match_roots = match_roots
        self.match_subtypes = match_subtypes

    def _matches_expansions(self, edge):
        for expansion in self.expansions:
            if edge_matches_pattern(edge, expansion):
                return True
        return False

    def _force_subtypes(self, edge):
        force_subtypes = False
        for st_pattern in self.match_subtypes:
            if edge_matches_pattern(edge, st_pattern):
                force_subtypes = True
        return force_subtypes

    def _force_root_expansion(self, edge):
        force_root = False
        force_expansion = False
        for root_pattern in self.match_roots:
            if edge_matches_pattern(edge, root_pattern):
                force_root = True
                force_expansion = True
            elif inner_edge_matches_pattern(edge, root_pattern):
                force_expansion = True
        return force_root, force_expansion

    def _list2patterns(self, ledge, depth=1, force_expansion=False,
                       force_root=False, force_subtypes=False):
        if depth > self.depth:
            return []

        first = ledge[0]

        f_force_subtypes = force_subtypes | self._force_subtypes(first)

        f_force_root, f_force_expansion = self._force_root_expansion(first)
        f_force_root |= force_root
        f_force_expansion |= force_expansion
        root = force_root | f_force_root

        if f_force_expansion and not first.atom:
            hpats = []
        else:
            hpats = [edge2pattern(first, root=root, subtype=f_force_subtypes)]

        if not first.atom and (self._matches_expansions(first) or
                                    f_force_expansion):
            hpats += self._list2patterns(
                list(first), depth + 1, force_expansion=f_force_expansion,
                force_root=f_force_root, force_subtypes=f_force_subtypes)
        if len(ledge) == 1:
            patterns = [[hpat] for hpat in hpats]
        else:
            patterns = []
            for pattern in self._list2patterns(
                    ledge[1:], depth=depth, force_expansion=force_expansion,
                    force_root=force_root, force_subtypes=force_subtypes):
                for hpat in hpats:
                    patterns.append([hpat] + pattern)
        return patterns

    def _edge2patterns(self, edge):
        force_subtypes = self._force_subtypes(edge)
        force_root, _ = self._force_root_expansion(edge)
        return list(hedge(pattern)
                    for pattern
                    in self._list2patterns(list(edge.normalized()),
                                           force_subtypes=force_subtypes,
                                           force_root=force_root,
                                           force_expansion=False))

    def count(self, edge):
        if edge.not_atom:
            if self._matches_expansions(edge):
                for pattern in self._edge2patterns(edge):
                    self.patterns[hedge(pattern)] += 1
            if self.count_subedges:
                for subedge in edge:
                    self.count(subedge)
