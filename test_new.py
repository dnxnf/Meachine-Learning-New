def solve(xiran, sanqiu):
    from collections import deque

    player_xiran = deque(xiran)
    player_sanqiu = deque(sanqiu)
    table = []
    turn = 'sanqiu'  # 叁秋先出

    while True:
        if turn == 'sanqiu':
            if not player_sanqiu:
                return 'xiran', list(player_xiran)
            card = player_sanqiu.popleft()
            current_player = player_sanqiu
            opponent_player = player_xiran
            next_turn = 'xiran'
        else:
            if not player_xiran:
                return 'sanqiu', list(player_sanqiu)
            card = player_xiran.popleft()
            current_player = player_xiran
            opponent_player = player_sanqiu
            next_turn = 'sanqiu'

        table.append(card)
        # print(f"{turn} 出牌: {card}, 桌面: {table}")

        # 检查是否出J
        if card == 'J':
            # 收走桌面所有牌
            while table:
                current_player.append(table.pop())
            # 收牌后检查对手是否还有牌
            if (turn == 'sanqiu' and not player_xiran) or (turn == 'xiran' and not player_sanqiu):
                return turn, list(current_player)
            # 出J后不换人，继续由当前玩家出牌
            continue

        # 检查是否有相同牌
        found_index = -1
        for i in range(len(table) - 1):  # 不包括刚出的这张牌
            if table[i] == card:
                found_index = i
                break

        if found_index != -1:
            # 收走从匹配牌到当前牌的所有牌
            captured = table[found_index:]
            table = table[:found_index]
            # 将收走的牌加入当前玩家手牌（按出牌顺序的逆序）
            for c in captured:
                current_player.append(c)
            # 收牌后检查对手是否还有牌
            if (turn == 'sanqiu' and not player_xiran) or (turn == 'xiran' and not player_sanqiu):
                return turn, list(current_player)
            # 收牌后不换人，继续由当前玩家出牌
            continue

        # 正常情况换人
        turn = next_turn


def commit():
    arr = input().strip()

    # 处理输入字符串，将10转换为'10'
    lst = []
    i = 0
    while i < len(arr):
        if arr[i] == '1' and i + 1 < len(arr) and arr[i + 1] == '0':
            lst.append('10')
            i += 2
        else:
            lst.append(arr[i])
            i += 1

    # 分配手牌：叁秋拿偶数索引，溪染拿奇数索引
    sanqiu = [lst[x] for x in range(0, min(52, len(lst)), 2)]
    xiran = [lst[x] for x in range(1, min(52, len(lst)), 2)]

    # print("溪染手牌:", xiran)
    # print("叁秋手牌:", sanqiu)

    winner, remaining_cards = solve(xiran, sanqiu)
    print(winner)
    print(' '.join(remaining_cards))


if __name__ == "__main__":
    commit()