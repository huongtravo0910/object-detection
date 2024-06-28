import streamlit as st


def levenshtein_distance(source, target):
    m, n = len(source), len(target)

    if m == 0:
        return n
    if n == 0:
        return m

    rows, cols = len(source) + 1, len(target) + 1
    matrix = [[i if j == 0 else 0 for j in range(rows)] for i in range(cols)]

    for j in range(rows):
        matrix[0][j] = j

    for i in range(1, cols):
        for j in range(1, rows):
            sub_cost = 0
            if source[j-1] != target[i-1]:
                sub_cost = 1

            matrix[i][j] = min(
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + sub_cost
            )

    return matrix[cols-1][rows-1]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path='data/vocab.txt')


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distences)


if __name__ == "__main__":
    main()
    # print(levenshtein_distance("elmets", "elements"))
