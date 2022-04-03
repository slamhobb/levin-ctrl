import concurrent.futures


def run_parallel(tasks: list, params: list):
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(0, len(tasks)):
            task = tasks[i]
            param = params[i]

            if param is None:
                future = executor.submit(task)
            else:
                future = executor.submit(task, param)

            futures.append(future)

        concurrent.futures.wait(futures)

        for future in futures:
            data = future.result()
            results.append(data)

        return results
