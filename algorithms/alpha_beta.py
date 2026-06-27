# Thuat toan Alpha-Beta Pruning cho co Caro 3x3

from algorithms.minimax import check_winner

def alpha_beta_decision(board, ai_player):
    """
    Tim nuoc di tot nhat cho AI su dung thuat toan Alpha-Beta Pruning.
    ai_player: 'X' hoac 'O'
    Tra ve: (best_move, best_score, nodes_evaluated, pruned_count, move_scores)
    - best_move: tuple (row, col)
    - best_score: diem so tot nhat (int)
    - nodes_evaluated: so luong trang thai da duyet
    - pruned_count: so luong nhanh bi cat tia
    - move_scores: danh sach cac nuoc di kha thi kem diem so tuong ung
    """
    opponent = 'O' if ai_player == 'X' else 'X'
    nodes_evaluated = [0]
    pruned_count = [0]
    
    def evaluate(board):
        winner = check_winner(board)
        if winner == ai_player:
            return 10
        elif winner == opponent:
            return -10
        elif winner == 'Tie':
            return 0
        return None

    def alphabeta(board, depth, alpha, beta, is_maximizing):
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
                        val = alphabeta(board, depth + 1, alpha, beta, False)
                        board[r][c] = ' '
                        best_val = max(best_val, val)
                        alpha = max(alpha, best_val)
                        if beta <= alpha:
                            pruned_count[0] += 1
                            break
                if beta <= alpha:
                    break
            return best_val
        else:
            best_val = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = opponent
                        val = alphabeta(board, depth + 1, alpha, beta, True)
                        board[r][c] = ' '
                        best_val = min(best_val, val)
                        beta = min(beta, best_val)
                        if beta <= alpha:
                            pruned_count[0] += 1
                            break
                if beta <= alpha:
                    break
            return best_val

    best_score = -float('inf')
    best_move = None
    move_scores = []
    alpha = -float('inf')
    beta = float('inf')
    
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = ai_player
                score = alphabeta(board, 0, alpha, beta, False)
                board[r][c] = ' '
                move_scores.append(((r, c), score))
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                # Cap nhat alpha cho nhanh goc
                alpha = max(alpha, best_score)
                    
    # Sap xep nuoc di co diem cao len truoc
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return best_move, best_score, nodes_evaluated[0], pruned_count[0], move_scores
