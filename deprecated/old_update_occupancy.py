def old_update_occupancy(self, player: Player):

    map_size = self.env_cfg.map_size
    queue = collections.deque([])
    for r in range(map_size):
        for c in range(map_size):
            if (r in [0, map_size-1] or c in [0, map_size-1]) and (self.grid[r][c] in [UNOCCUPIED, BOMB, BOOST]):
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if 0<=r<map_size and 0<=c<map_size and (self.grid[r][c] in [UNOCCUPIED, BOMB, BOOST]):
            if (self.grid[r][c] == UNOCCUPIED): self.grid[r][c] = TEMP
            if (self.grid[r][c] == BOMB): self.grid[r][c] = -1 * BOMB
            if (self.grid[r][c] == BOOST): self.grid[r][c] = -1 * BOOST
            queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])

    for r in range(map_size):
        for c in range(map_size):
            cell = self.grid[r][c]
            occupied_by = self.player_grid[r][c]
            if (occupied_by == player and cell == PASSED) or (cell in [UNOCCUPIED, BOMB, BOOST]):
                self.grid[r][c] = OCCUPIED
                self.player_grid[r][c] = player
                self.player_num_grid[r][c] = player.num
                player.push_zone((c,r))
            elif cell == TEMP:
                self.grid[r][c] = UNOCCUPIED
                self.player_grid[r][c] = None
                self.player_num_grid[r][c] = -1
            elif cell == -1 * BOMB:
                self.grid[r][c] = BOMB
                self.player_grid[r][c] = None
                self.player_num_grid[r][c] = -1
            elif cell == -1 * BOOST:
                self.grid[r][c] = BOOST
                self.player_grid[r][c] = None
                self.player_num_grid[r][c] = -1