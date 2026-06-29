# Thuat toan Minimax cho co Caro 3x3

def check_winner(board):

    win_states = [
        # Hang ngang
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Cot doc
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Duong cheo
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    
    for state in win_states:
        p1, p2, p3 = state
        if board[p1[0]][p1[1]] != ' ' and board[p1[0]][p1[1]] == board[p2[0]][p2[1]] == board[p3[0]][p3[1]]:
            return board[p1[0]][p1[1]]
            
    # Kiem tra neu con o trong thi chua ket thuc
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                return None
                
    return 'Tie'

def minimax_decision(board, ai_player):
    
    opponent = 'O' if ai_player == 'X' else 'X'
    nodes_evaluated = [0]
    
    def evaluate(board):
        winner = check_winner(board)
        if winner == ai_player:
            return 10
        elif winner == opponent:
            return -10
        elif winner == 'Tie':
            return 0
        return None

    def minimax(board, is_maximizing):
        nodes_evaluated[0] += 1
        score = evaluate(board)
        if score is not None:
            return score
            
        if is_maximizing:
            best_val = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = ai_player
                        val = minimax(board, False)
                        board[r][c] = ' '
                        best_val = max(best_val, val)
            return best_val
        else:
            best_val = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = opponent
                        val = minimax(board, True)
                        board[r][c] = ' '
                        best_val = min(best_val, val)
            return best_val

    best_score = -float('inf')
    best_move = None
    move_scores = []
    
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = ai_player
                score = minimax(board, False)
                board[r][c] = ' '
                move_scores.append(((r, c), score))
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                    
    # Sap xep nuoc di co diem cao len truoc
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return best_move, best_score, nodes_evaluated[0], move_scores
