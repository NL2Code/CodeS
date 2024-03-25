# Copyright (c) Microsoft Corporation.
# Copyright (c) 2023 Konstantin Chernyshev.
# Licensed under the MIT license.
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union
import math

from . import bleu, dataflow_match, syntax_match, weighted_ngram_match

PACKAGE_DIR = Path(__file__).parent
AVAILABLE_LANGS = ["java", "javascript", "c_sharp", "php", "c", "cpp", "python", "go", "ruby"]  # keywords available


def calc_codebleu(
    references: Union[List[str], List[List[str]]],
    predictions: List[str],
    lang: str,
    weights: Tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
    tokenizer: Optional[Callable] = None,
    keywords_dir: Path = PACKAGE_DIR / "keywords",
    lang_so_file: Path = PACKAGE_DIR / "my-languages.so",
) -> Dict[str, float]:
    """Calculate CodeBLEU score

    Args:
        predictions: list of predictions
        references: list of lists with references
        lang: input language, one of AVAILABLE_LANGS
        weights: weights of the ngram_match, weighted_ngram_match, syntax_match, and dataflow_match respectively
        tokenizer: tokenizer function, Defaults to lambda s: s.split()
        keywords_dir: path to the directory with keywords files
        lang_so_file: path to the .so file with the parser for the language

    Return:
        Scores dict
    """
    assert len(references) == len(predictions), "Number of references and predictions should be the same"
    assert lang in AVAILABLE_LANGS, f"Language {lang} is not supported (yet). Available languages: {AVAILABLE_LANGS}"
    assert len(weights) == 4, "weights should be a tuple of 4 floats (alpha, beta, gamma, theta)"
    assert keywords_dir.exists(), f"keywords_dir {keywords_dir} does not exist"
    assert lang_so_file.exists(), f"lang_so_file {lang_so_file} does not exist"

    # preprocess inputs
    references = [[x.strip() for x in ref] if isinstance(ref, list) else [ref.strip()] for ref in references]
    hypothesis = [x.strip() for x in predictions]

    # calculate ngram match (BLEU)
    if tokenizer is None:

        def tokenizer(s):
            return s.split()

    tokenized_hyps = [tokenizer(x) for x in hypothesis]
    tokenized_refs = [[tokenizer(x) for x in reference] for reference in references]

    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)

    # calculate weighted ngram match
    with open(keywords_dir / (lang + ".txt"), "r", encoding="utf-8") as f:
        keywords = [x.strip() for x in f.readlines()]

    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}

    tokenized_refs_with_weights = [
        [[reference_tokens, make_weights(reference_tokens, keywords)] for reference_tokens in reference]
        for reference in tokenized_refs
    ]

    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(tokenized_refs_with_weights, tokenized_hyps)

    # calculate syntax match
    syntax_match_score = syntax_match.corpus_syntax_match(references, hypothesis, lang, str(lang_so_file))

    # calculate dataflow match
    dataflow_match_score = dataflow_match.corpus_dataflow_match(references, hypothesis, lang, str(lang_so_file))

    alpha, beta, gamma, theta = weights
    code_bleu_score = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score
        + theta * (dataflow_match_score or 1)
    )

    return {
        "codebleu": code_bleu_score,
        "ngram_match_score": ngram_match_score,
        "weighted_ngram_match_score": weighted_ngram_match_score,
        "syntax_match_score": syntax_match_score,
        "dataflow_match_score": dataflow_match_score,
    }


import os
import ast
from scipy.sparse import csr_matrix
from scipy.optimize import linear_sum_assignment


def stack_source_code(file_list: List[Path]) -> str:
    source_code = ""
    for file in file_list:
        with open(file, "r", encoding="utf-8") as f:
            source_code += f.read().strip() + "\n"

    return source_code


def get_file_list(dir: Path, ext: str) -> List[Path]:
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(ext):
                file_list.append(os.path.join(root, file))
    return file_list


def extract_functions(source):
    try:
        code_ast = ast.parse(source)
        functions = [node for node in ast.walk(code_ast) if isinstance(node, ast.FunctionDef)]
        function_sources = [ast.get_source_segment(source, function) for function in functions]
        return function_sources
    except:
        lines = source.split("\n")
        start = 0
        function_sources = []
        while start < len(lines):
            line = lines[start]
            if line.startswith("def "):
                end = start + 1
                while True:
                    if not lines[end].startswith(" ") and not lines[end].startswith("\t"):
                        function_sources.append("\n".join(lines[start:end]))
                        start = end
                        break
                    end += 1
            start += 1
        return function_sources


def calc_repobleu(
    reference_dirs: List[Path],
    prediction_dirs: List[Path],
    lang: str,
    weights: Tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
    tokenizer: Optional[Callable] = None,
    keywords_dir: Path = PACKAGE_DIR / "keywords",
    lang_so_file: Path = PACKAGE_DIR / "my-languages.so",
) -> Dict[str, float]:
    """Calculate CodeBLEU score

    Args:
        reference_dirs: list of directories with references
        prediction_dirs: list of directories with predictions
        lang: input language, one of AVAILABLE_LANGS
        weights: weights of the ngram_match, weighted_ngram_match, syntax_match, and dataflow_match respectively
        tokenizer: tokenizer function, Defaults to lambda s: s.split()
        keywords_dir: path to the directory with keywords files
        lang_so_file: path to the .so file with the parser for the language

    Return:
        Scores dict
    """
    assert len(reference_dirs) == len(
        prediction_dirs
    ), "Number of reference and prediction directories should be the same"
    assert lang in AVAILABLE_LANGS, f"Language {lang} is not supported (yet). Available languages: {AVAILABLE_LANGS}"
    assert len(weights) == 4, "weights should be a tuple of 4 floats (alpha, beta, gamma, theta)"
    assert keywords_dir.exists(), f"keywords_dir {keywords_dir} does not exist"
    assert lang_so_file.exists(), f"lang_so_file {lang_so_file} does not exist"

    # preprocess inputs
    references = []
    predictions = []
    for reference_dir, prediction_dir in zip(reference_dirs, prediction_dirs):
        assert reference_dir.exists(), f"reference_dir {reference_dir} does not exist"
        assert prediction_dir.exists(), f"prediction_dir {prediction_dir} does not exist"
        reference_files = get_file_list(reference_dir, ".py")
        prediction_files = get_file_list(prediction_dir, ".py")

        reference_source = stack_source_code(reference_files)
        prediction_source = stack_source_code(prediction_files)

        references.append(reference_source)
        predictions.append(prediction_source)

    # calculate ngram match (BLEU)
    if tokenizer is None:

        def tokenizer(s):
            return s.split()

    tokenized_hyps = [tokenizer(x) for x in predictions]
    tokenized_refs = [[tokenizer(x)] for x in references]

    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)

    # calculate weighted ngram match
    with open(keywords_dir / (lang + ".txt"), "r", encoding="utf-8") as f:
        keywords = [x.strip() for x in f.readlines()]

    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}

    tokenized_refs_with_weights = [
        [[reference_tokens, make_weights(reference_tokens, keywords)] for reference_tokens in reference]
        for reference in tokenized_refs
    ]
    tokenized_hyps_with_weights = [
        [hypothesis_tokens, make_weights(hypothesis_tokens, keywords)] for hypothesis_tokens in tokenized_hyps
    ]

    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(
        tokenized_refs_with_weights, tokenized_hyps_with_weights
    )

    # calculate syntax match
    syntax_match_score = syntax_match.repo_syntax_match([reference_dirs], prediction_dirs, lang, str(lang_so_file))

    # calculate dataflow match
    ref_functions = [extract_functions(ref) for ref in references]
    hyp_functions = [extract_functions(hyp) for hyp in predictions]
    results = []
    for case in range(len(ref_functions)):
        data = []
        row = []
        col = []
        refs = ref_functions[case]
        hyps = hyp_functions[case]
        for i, ref in enumerate(refs):
            for j, hyp in enumerate(hyps):
                df_value = dataflow_match.corpus_dataflow_match([[ref]], [hyp], lang, str(lang_so_file))
                if df_value != 0:
                    data.append(df_value)
                    row.append(i)
                    col.append(j)
        biadjacency_matrix = csr_matrix((data, (row, col)))
        row_ind, col_ind = linear_sum_assignment(biadjacency_matrix.toarray(), maximize=True)
        dataflow_match_score = biadjacency_matrix[row_ind, col_ind].sum()

        def getBP(closest_ref_len, hyp_len):
            if 2 * hyp_len > closest_ref_len:
                return 1
            # If hypothesis is empty, brevity penalty = 0 should result in BLEU = 0.0
            elif hyp_len == 0:
                return 0
            else:
                # return math.exp(1 - closest_ref_len / hyp_len)
                return 1 / (1 + math.log(closest_ref_len / (2 * hyp_len)))

        bp = min(getBP(len(refs), len(hyps)), getBP(len(hyps), len(refs)))
        results.append(dataflow_match_score / min(len(refs), len(hyps)) * bp)
    dataflow_match_score = sum(results) / len(results)

    alpha, beta, gamma, theta = weights
    code_bleu_score = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score
        + theta * (dataflow_match_score or 1)
    )

    return {
        "codebleu": code_bleu_score,
        "ngram_match_score": ngram_match_score,
        "weighted_ngram_match_score": weighted_ngram_match_score,
        "syntax_match_score": syntax_match_score,
        "dataflow_match_score": dataflow_match_score,
    }
