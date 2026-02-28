import shlex
import subprocess
from pathlib import Path
from config import SEARCH_ROOTS, TOP_N

def run_cmd(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout.strip()

def mdfind_query(query: str, roots: list[str], top_n: int) -> list[str]:
    """
    Spotlight로 '내용+메타데이터' 검색.
    -onlyin 으로 범위를 제한해 정확도 상승.
    """
    results: list[str] = []

    # 여러 root를 돌며 결과를 누적 (root별로 -onlyin 적용)
    for root in roots:
        root = str(Path(root).expanduser())
        cmd = ["mdfind", "-onlyin", root, query]
        out = run_cmd(cmd)
        if out:
            results.extend(out.splitlines())

    # 중복 제거 + 상위 N개
    uniq = []
    seen = set()
    for p in results:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
        if len(uniq) >= top_n:
            break
    return uniq

def mdls_fields(path: str) -> dict:
    """
    macOS 메타데이터 일부를 가져와서 출력에 활용(파일명/종류/생성일 등).
    """
    # 필요한 키만 뽑아 간단히
    keys = ["kMDItemDisplayName", "kMDItemKind", "kMDItemFSContentChangeDate"]
    cmd = ["mdls"] + [f"-name" for _ in keys]
    # mdls는 -name을 여러 번 받습니다.
    # ["mdls","-name","k1","-name","k2",...,"path"] 형태로 구성
    cmd = ["mdls"]
    for k in keys:
        cmd += ["-name", k]
    cmd.append(path)

    out = run_cmd(cmd)
    info = {}
    for line in out.splitlines():
        if " = " in line:
            k, v = line.split(" = ", 1)
            info[k.strip()] = v.strip()
    return info

def main():
    print("macOS 로컬 파일 찾기 에이전트 (Spotlight 기반)")
    print("검색 범위:", ", ".join(SEARCH_ROOTS))
    print()

    while True:
        q = input("찾고 싶은 파일을 자연어로 입력하세요 (종료: q): ").strip()
        if not q or q.lower() == "q":
            break

        # mdfind는 자연어도 어느 정도 먹히지만,
        # 너무 긴 문장은 핵심 키워드만 남기는 게 더 잘 맞는 경우가 있습니다.
        # ('그냥 자연어로도 되지만, 핵심 단어가 더 정확')
        results = mdfind_query(q, SEARCH_ROOTS, TOP_N)

        if not results:
            print("❌ 결과 없음. (키워드를 더 구체화해보세요)\n")
            continue

        print("\n📁 후보 파일:")
        for i, path in enumerate(results, 1):
            meta = mdls_fields(path)
            name = meta.get("kMDItemDisplayName", "").strip('"')
            kind = meta.get("kMDItemKind", "").strip('"')
            changed = meta.get("kMDItemFSContentChangeDate", "")
            print(f"{i}. {name} | {kind} | {changed}")
            print(f"   {path}")

        print("\n정밀 파일 검색이 완료되었습니다.\n")
        # 결과 출력 직후에 추가하세요 (results가 있는 상태)

        # ✅ 결과 중 하나를 Finder에서 열거나, 파일을 기본 앱으로 열기
        action = input("동작 선택: [r] Finder에서 위치 표시 / [o] 파일 열기 / [Enter] 건너뜀: ").strip().lower()
        if action in {"r", "o"}:
            choice = input(f"번호 입력 (1~{len(results)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    target = results[idx]
                    if action == "r":
                        subprocess.run(["open", "-R", target])  
                        # ✅ Finder에서 위치 표시(파일 선택)
                    else:
                        subprocess.run(["open", target])        
                        # ✅ 기본 앱으로 파일 열기(동영상은 QuickTime 등)
                else:
                    print("번호가 범위를 벗어났습니다.\n")
            else:
                print("숫자를 입력해주세요.\n")

if __name__ == "__main__":
    main()