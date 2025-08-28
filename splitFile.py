import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Split a file into smaller files.")
    parser.add_argument("--file", required=True, help="Path to the input file.")
    parser.add_argument("--splitkb", type=int, required=True,
                        help="Size in kilobytes to split the file by.")

    args = parser.parse_args()

    input_filepath = os.path.abspath(args.file)
    split_size_kb = args.splitkb

    if not os.path.exists(input_filepath):
        print(f"오류: 파일을 찾을 수 없습니다: {input_filepath}")
        sys.exit(1)

    if not os.path.isfile(input_filepath):
        print(f"오류: '{input_filepath}'은(는) 파일이 아닙니다.")
        sys.exit(1)

    if split_size_kb <= 0:
        print("오류: --splitkb 값은 0보다 커야 합니다.")
        sys.exit(1)

    # Read file in binary mode to detect encoding
    try:
        with open(input_filepath, 'rb') as f:
            raw_bytes = f.read()
    except IOError as e:
        print(f"오류: 파일을 읽는 중 문제가 발생했습니다: {e}")
        sys.exit(1)

    # Attempt to decode with common encodings
    decoded_content = None
    encodings_to_try = ['utf-8', 'euc-kr', 'cp949', 'latin-1'] 
    
    for encoding in encodings_to_try:
        try:
            decoded_content = raw_bytes.decode(encoding)
            break # Successfully decoded
        except UnicodeDecodeError:
            continue # Try next encoding
    
    if decoded_content is None:
        print("오류: 텍스트 내용 파일이 아닙니다. (지원되는 인코딩으로 디코딩할 수 없습니다)")
        sys.exit(1)

    # Ensure content is UTF-8 encoded for splitting
    # If it was already decoded, it's a string, so encode it to utf-8 bytes
    utf8_encoded_bytes = decoded_content.encode('utf-8')

    # Prepare for splitting
    file_dir = os.path.dirname(input_filepath)
    file_basename = os.path.basename(input_filepath)
    filename_without_ext, file_extension = os.path.splitext(file_basename)

    split_size_bytes = split_size_kb * 1024
    total_bytes = len(utf8_encoded_bytes)
    
    if total_bytes == 0:
        print("경고: 입력 파일이 비어 있습니다. 분할할 내용이 없습니다.")
        sys.exit(0)

    num_splits = (total_bytes + split_size_bytes - 1) // split_size_bytes
    
    print(f"'{input_filepath}' 파일을 {split_size_kb}KB 크기로 분할합니다...")
    print(f"총 {num_splits}개의 파일이 생성될 예정입니다.")

    created_files = []
    for i in range(num_splits):
        start_byte = i * split_size_bytes
        end_byte = min((i + 1) * split_size_bytes, total_bytes)
        chunk = utf8_encoded_bytes[start_byte:end_byte]

        output_filename = f"{filename_without_ext}.{i+1}{file_extension}"
        output_filepath = os.path.join(file_dir, output_filename)

        try:
            with open(output_filepath, 'wb') as out_f:
                out_f.write(chunk)
            created_files.append(output_filepath)
        except IOError as e:
            print(f"오류: 파일 '{output_filepath}'을(를) 쓰는 중 문제가 발생했습니다: {e}")
            pass 
    
    if created_files:
        print(f"파일 분할이 완료되었습니다. {len(created_files)}개의 파일이 생성되었습니다:")
        for f in created_files:
            print(f"- {f}")
    else:
        print("경고: 파일을 생성하지 못했습니다.")

if __name__ == "__main__":
    main()
