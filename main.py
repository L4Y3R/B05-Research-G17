import TemperatureStudy

async def main():
    study = TemperatureStudy()
    results = await study.run_study()
    analysis = study.analyze_results(results)
    print(analysis)

if __name__ == "__main__":
    asyncio.run(main())