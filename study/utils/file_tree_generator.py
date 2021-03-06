class FileTreeGenerator:

    def __init__(self):
        self.tree = []

    def put_all(self, file_paths):
        for file_path in file_paths:
            self.put(file_path)
        return self

    def put(self, file_path):
        split_file_path = file_path.split('/')
        self.recursive_put(self.tree, split_file_path, split_file_path)
        return self

    def recursive_put(self, tree, split_file_path, full_split_file_path):
        if len(split_file_path) > 1:
            if split_file_path[0] in map(lambda node: node['name'], tree):
                node_dict = list(filter(lambda node: node['name'] == split_file_path[0], tree))[0]
            else:
                node_dict = {
                    'name': split_file_path[0],
                    'children': [],
                }
                if 'filepath' not in node_dict:
                    curr_index = full_split_file_path.index(node_dict['name'])
                    node_dict['filepath'] = '/'.join(full_split_file_path[:curr_index + 1])
                tree.append(node_dict)
            self.recursive_put(node_dict['children'], split_file_path[1:], full_split_file_path)
        elif split_file_path[0] != '':
            tree.append({
                'name': split_file_path[0],
                'filepath': '/'.join(full_split_file_path),
            })
