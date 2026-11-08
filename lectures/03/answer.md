# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
    素のLLMは一般論で答えたが、エージェントはdata/glossary.jsonを使って答えていた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：
     requests=2
- 追加したツールと、docstring に書いた説明：
    def make_quiz(lecture: int) -> str:
    """指定した回の用語から1つ選び、確認問題と答えを返す。
    学習者が特定の回の復習や理解確認のために問題を求めたときに使う。
    用語の定義を問う問題を出し、答え合わせに使える定義も返す。
    """
    terms = [term for term in load_glossary() if term["lecture"] == lecture]
    if not terms:
        return f"第{lecture}回の用語は用語集にありません。"

    term = random.choice(terms)
    return json.dumps(
        {
            "lecture": lecture,
            "term": term["term"],
            "question": f"「{term['term']}」とは何ですか？",
            "answer": term["definition"],
        },
        ensure_ascii=False,
    )
## 宿題

- 取り組んだレベル：基礎
- やったこと：docstring の「用語を1つだけ入れる」を「まとめて入れる」に変えた
- 結果：
　「1つだけ」requests=2, tool_calls=2
　「まとめて」 requests=2, tool_calls=1
- 気づき・疑問：
　「まとめて」だと tool_callsが1回になりコスト面ではいいのかもしれないが、まとめて検索することで挙動に問題が出ることはあるのか疑問に思った。
