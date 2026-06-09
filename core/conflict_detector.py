class ConflictDetector:

    @staticmethod
    def find_conflicts(events):

        conflicts = []

        sorted_events = sorted(
            events,
            key=lambda e: e.start_datetime
        )

        for i in range(len(sorted_events) - 1):

            current = sorted_events[i]
            next_event = sorted_events[i + 1]

            if current.end_datetime > next_event.start_datetime:

                conflicts.append(
                    (
                        current.subject,
                        next_event.subject
                    )
                )

        return conflicts