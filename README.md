                         CLIENT
                            │
                            ▼
                         FASTAPI
                            │
                    Request Validation
                         (Pydantic)
                            │
                            ▼
                         REDIS
                      Cache Lookup
                       │         │
                    HIT │         │ MISS
                       ▼         ▼
                   Return     POSTGRESQL
                                  │
                            FOUND │ NOT FOUND
                                  │      │
                                  ▼      ▼
                             Redis    HTTP FETCH
                                        │
                                   asyncio.gather
                                        │
                                   Semaphore
                                        │
                                        ▼
                                   PostgreSQL
                                        │
                                        ▼
                                      Redis
                                        │
                                        ▼
                                      Response