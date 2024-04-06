import sys

def run():

    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    match fetch_script:
        case "t212history":
            from lifehub.app.fetch_scripts.t212history import T212HistoryFetch
            T212HistoryFetch().fetch()
        case "networth":
            from lifehub.app.fetch_scripts.networth import NetworthFetch
            NetworthFetch().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")

if __name__ == "__main__":
    run()
