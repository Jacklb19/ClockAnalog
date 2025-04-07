import datetime

class ClockSegment:
    def __init__(self, time_value):
        self.time_value = time_value
        self.prev = None
        self.next = None

class ClockCircularList:
    def __init__(self):
        self.head = None

    def insert_segment_at_end(self, time_value):
        new_segment = ClockSegment(time_value)
        if self.head is None:
            self.head = new_segment
            new_segment.next = self.head
            new_segment.prev = self.head
        else:
            last = self.head.prev 
            last.next = new_segment
            new_segment.prev = last
            new_segment.next = self.head
            self.head.prev = new_segment
        
    def print_segments(self):
        if self.head is None:
            print("La lista de segmentos está vacía.")
            return
        
        current = self.head
        print(current.time_value)
        current = current.next
        while current != self.head:
            print(current.time_value)
            current = current.next

    # Obtener el segmento correspondiente a la hora actual (en formato de 12 horas)
    def get_current_hour_segment(self):
        current_hour = datetime.datetime.now().hour % 12
        if current_hour == 0:
            current_hour = 12
        return self.find_segment(current_hour)

    def find_segment(self, hour_value):
        if self.head is None:
            return None
        current = self.head
        while True:
            if current.time_value == hour_value:
                return current
            current = current.next
            if current == self.head:
                break
        return None

if __name__ == "__main__":
    clock_segments = ClockCircularList()
    
    # horas insertadas
    for i in range(1, 13):
        clock_segments.insert_segment_at_end(i)
    
    clock_segments.print_segments()

    # mostrar hora actual
    current_segment = clock_segments.get_current_hour_segment()
    if current_segment:
        print(f"\nHora actual (segmento): {current_segment.time_value}")
