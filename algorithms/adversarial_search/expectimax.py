# Thuat toan Expectimax cho co Caro 3x3

from algorithms.adversarial_search.minimax import check_winner

def expectimax_decision(board, ai_player):

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

    def expectimax(board, is_maximizing):
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
                        val = expectimax(board, False)
                        board[r][c] = ' '
                        best_val = max(best_val, val)
            return best_val
        else:
            # Chance node: Tinh trung binh cong tat ca cac nuoc di cua doi thu
            total_val = 0.0
            count = 0
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = opponent
                        val = expectimax(board, True)
                        board[r][c] = ' '
                        total_val += val
                        count += 1
            if count == 0:
                return 0.0
            return total_val / count

    best_score = -float('inf')
    best_move = None
    move_scores = []
    
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = ai_player
                score = expectimax(board, False)
                board[r][c] = ' '
                move_scores.append(((r, c), round(score, 2)))
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                    
    # Sap xep nuoc di co diem cao len truoc
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return best_move, best_score, nodes_evaluated[0], move_scores
