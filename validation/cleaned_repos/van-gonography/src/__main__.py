import sys

if __name__ == "__main__":
    # Check for python version 3.6 or higher
    if sys.version_info < (3, 6):
        sys.exit("vangonography requires Python 3.6 or higher")

    try:
        import vangonography

        vangonography.main()
    except Exception as e:
        print(f"An error occurred: {e}")
