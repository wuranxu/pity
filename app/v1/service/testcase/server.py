import asyncio
import sys

sys.path.append(r"../../../../")

from app.utils.serve import RpcService
from app.v1.service.dashboard.api.DashboardService import DashboardServiceApi
from app.v1.service.dashboard.proto import dashboard_pb2_grpc, dashboard_pb2


async def main():
    await RpcService.start("./service.yml", dashboard_pb2_grpc.add_dashboardServicer_to_server, DashboardServiceApi(),
                           dashboard_pb2)


if __name__ == "__main__":
    asyncio.run(main())
