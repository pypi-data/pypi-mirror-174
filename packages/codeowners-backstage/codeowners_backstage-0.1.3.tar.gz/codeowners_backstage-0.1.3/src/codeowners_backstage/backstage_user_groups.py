
class BackstageUserGroups:
    @classmethod
    def load(cls, backstage_host, namespace, requests):
        url = f'{backstage_host}/api/catalog/entities?filter=kind=user,metadata.namespace={namespace}' \
              f'&filter=kind=group,metadata.namespace={namespace}&fields=kind,metadata.name,spec.profile.email,relations'
        response = requests.get(url)
        response.raise_for_status()
        return BackstageUserGroups(response.json())

    def __init__(self, backstage_json):
        self._entities_by_name = {e['metadata']['name']: e for e in backstage_json}

    def get_group_members_iter(self, group_name):
        try:
            group = self._entities_by_name[group_name]
        except KeyError:
            yield from ()
        else:
            group_member_names = [rel['target']['name'] for rel in group['relations'] if rel['type'] == 'hasMember']
            child_group_names = [rel['target']['name'] for rel in group['relations'] if rel['type'] == 'parentOf']

            for member_name in group_member_names:
                yield self._entities_by_name[member_name]['spec']['profile']['email']

            for child_group_name in child_group_names:
                yield from self.get_group_members_iter(child_group_name)

    def get_group_members(self, group_name):
        if group_name not in self._entities_by_name:
            return None
        return list(self.get_group_members_iter(group_name))


class GroupNotFoundError(Exception):
    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self) -> str:
        return f"GroupNotFoundError: {self.group_name}"


