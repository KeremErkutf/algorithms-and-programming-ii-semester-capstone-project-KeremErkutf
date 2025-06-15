import collections

class Graph:
    def __init__(self, num_vertices):
        """
        Grafı başlatır.
        Args:
            num_vertices (int): Grafteki toplam düğüm sayısı.
        """
        self.num_vertices = num_vertices
        self.adj = collections.defaultdict(list) # Komşuluk listesi
        self.in_degree = collections.defaultdict(int) # Gelen kenar (in-degree) sayısı

    def add_edge(self, u, v):
        """
        Grafa yönlü bir kenar ekler (u -> v).
        Args:
            u (int): Başlangıç düğümü.
            v (int): Bitiş düğümü.
        """
        self.adj[u].append(v)
        self.in_degree[v] += 1
        # Henüz in-degree'si olmayan düğümler için başlangıç değerini 0 olarak ayarla
        if u not in self.in_degree:
            self.in_degree[u] = 0
        if v not not in self.adj: # Eğer v düğümü henüz komşuluk listesinde yoksa ekle (in-degree'si 0 olsa bile)
            self.adj[v] = []

    def get_vertices(self):
        """Grafın tüm düğümlerini döndürür."""
        # Tüm düğümleri bulmak için hem adj hem de in_degree'yi kontrol et
        all_vertices = set(self.adj.keys())
        for destinations in self.adj.values():
            all_vertices.update(destinations)
        return sorted(list(all_vertices))


def topological_sort_kahn(graph):
    """
    Kahn's algoritmasını kullanarak topolojik sıralama yapar.
    Args:
        graph (Graph): Sıralanacak Graph nesnesi.

    Returns:
        tuple: (list: Topolojik sıralanmış düğümler, list: Adım adım işlem geçmişi, bool: Döngü tespit edildi mi)
    """
    sorted_order = []
    # Adım adım görselleştirme için işlem geçmişi
    # Her adımda: (açıklama, mevcut_kuyruk, işlenen_düğüm, guncellenen_in_degree, mevcut_sıralama)
    steps = []

    # Başlangıçta in-degree'si 0 olan tüm düğümleri bul
    # graph.in_degree sadece kenar gelenleri tuttuğu için, tüm düğümleri de kontrol etmek lazım
    # Özellikle in_degree'si 0 olan ama adj'de olmayan düğümler için
    queue = collections.deque()
    initial_in_degrees = {v: graph.in_degree.get(v, 0) for v in graph.get_vertices()}

    for vertex in initial_in_degrees:
        if initial_in_degrees[vertex] == 0:
            queue.append(vertex)
            steps.append(f"Başlangıç: '{vertex}' düğümünün gelen kenarı 0, kuyruğa eklendi. Kuyruk: {list(queue)}, Sıralama: {sorted_order}")

    count = 0 # Topolojik sıralamaya eklenen düğüm sayısı

    while queue:
        u = queue.popleft()
        sorted_order.append(u)
        count += 1
        steps.append(f"Adım {count}: Kuyruktan '{u}' düğümü çıkarıldı ve sıralamaya eklendi. Kuyruk: {list(queue)}, Sıralama: {sorted_order}")

        # u'nun komşularının gelen kenar sayılarını azalt
        for v in graph.adj[u]:
            initial_in_degrees[v] -= 1
            steps.append(f"  -> '{u}' düğümünün komşusu '{v}' düğümünün gelen kenarı 1 azaltıldı. Yeni gelen kenar: {initial_in_degrees[v]}")
            if initial_in_degrees[v] == 0:
                queue.append(v)
                steps.append(f"  -> '{v}' düğümünün gelen kenarı 0 oldu, kuyruğa eklendi. Kuyruk: {list(queue)}")

    # Eğer sıralanan düğüm sayısı, toplam düğüm sayısından az ise döngü var demektir.
    has_cycle = count != len(graph.get_vertices())
    if has_cycle:
        steps.append("Döngü tespit edildi! Tüm düğümler topolojik olarak sıralanamadı.")
    else:
        steps.append("Tüm düğümler başarıyla topolojik olarak sıralandı.")


    return sorted_order, steps, has_cycle

# Testler için örnek kullanım (isteğe bağlı, kaldırılabilir veya test_algorithm.py'ye taşınabilir)
if __name__ == "__main__":
    print("Graf 1: Basit Sıralama")
    g1 = Graph(6)
    g1.add_edge(5, 2)
    g1.add_edge(5, 0)
    g1.add_edge(4, 0)
    g1.add_edge(4, 1)
    g1.add_edge(2, 3)
    g1.add_edge(3, 1)
    # Düğüm 0, 1, 2, 3, 4, 5 olmalı.
    # Eğer belirtilmemiş düğümler varsa (mesela sadece 0 ve 1 arasında kenar var ama 2 de var)
    # get_vertices metodu tüm düğümleri doğru döndürmeli
    # Bu durumda Graph'ı başlatırken num_vertices yerine add_edge ile dinamik düğüm ekleme mantığı daha iyi.
    # Yukarıdaki Graph sınıfı bu dinamizmi destekleyecek şekilde güncellendi.


    sorted_g1, steps_g1, has_cycle_g1 = topological_sort_kahn(g1)
    print("Sıralama:", sorted_g1)
    print("Döngü var mı?", has_cycle_g1)
    print("\nAdımlar:")
    for step in steps_g1:
        print(step)

    print("\n" + "="*30 + "\n")

    print("Graf 2: Döngü içeren")
    g2 = Graph(3) # 0, 1, 2
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 0) # Döngü!

    sorted_g2, steps_g2, has_cycle_g2 = topological_sort_kahn(g2)
    print("Sıralama:", sorted_g2)
    print("Döngü var mı?", has_cycle_g2)
    print("\nAdımlar:")
    for step in steps_g2:
        print(step)

    print("\n" + "="*30 + "\n")

    print("Graf 3: Bağımsız Düğümler")
    g3 = Graph(4) # 0, 1, 2, 3
    g3.add_edge(0, 1)
    g3.add_edge(2, 3) # 0-1 ve 2-3 ayrı parçalar
    # Düğüm 0,1,2,3 var ama 0 ve 2'nin in-degree'si 0, kuyruğa eklenecekler
    sorted_g3, steps_g3, has_cycle_g3 = topological_sort_kahn(g3)
    print("Sıralama:", sorted_g3)
    print("Döngü var mı?", has_cycle_g3)
    print("\nAdımlar:")
    for step in steps_g3:
        print(step)
