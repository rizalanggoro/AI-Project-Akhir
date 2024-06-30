import { AudioWaveform, Dices, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import { FormattedDate, FormattedNumber } from "react-intl";
import NavbarComponent from "./components/navbar";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { Badge } from "./components/ui/badge";
import { Button } from "./components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { apiBaseUrl } from "./lib/const";
import { Data } from "./lib/models";
import { cn } from "./lib/utils";

export default function App() {
  const [data, setData] = useState<Data[]>([]);
  const [filterData, setFilterData] = useState("-1");
  const [predictionData, setPredictionData] = useState({
    kasus_dbd: 10,
    temp_avg: 25.5,
    humidity_avg: 80,
    rainfall_rate: 15,
    kepadatan_penduduk: 15000,
    result: "",
    isLoading: false,
  });

  useEffect(() => {
    const getDatasetAfterClustering = async () => {
      const response = await fetch(apiBaseUrl + "dataset");
      if (response.ok) {
        const json = await response.json();
        setData(json);
      }
    };

    getDatasetAfterClustering();
  }, []);

  const onClickButtonPredict = async () => {
    try {
      setPredictionData({ ...predictionData, isLoading: true, result: "" });
      const response = await fetch(apiBaseUrl + "prediction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...predictionData,
        }),
      });

      const json = await response.json();

      setPredictionData({
        ...predictionData,
        isLoading: false,
        result: json.prediction,
      });
    } catch (e) {
      setPredictionData({
        ...predictionData,
        isLoading: false,
        result: "",
      });
    }
  };

  return (
    <>
      <NavbarComponent />
      <div className="max-w-5xl pt-24 pb-8 mx-auto">
        <div className="space-y-2">
          <p className="text-2xl font-bold">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              Penerapan Clustering K-Means dan KNN
            </span>{" "}
            dalam Prediksi Tingkat Kerentanan Harian Penyebaran Penyakit DBD di
            Jakarta Selatan
          </p>
          <p className="text-muted-foreground">
            Algoritma clustering K-Means digunakan untuk mengelompokkan data
            berdasarkan kesamaan variabel. Kemudian, algoritma KNN digunakan
            untuk memprediksi tingkat kerentanan harian penyebaran DBD dengan
            mengidentifikasi tetangga terdekat dalam kelompok-kelompok tersebut.
          </p>
        </div>

        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="text-lg">Prediksi</CardTitle>
            <CardDescription>
              Masukkan beberapa informasi berikut untuk memprediksi tingkat
              kerentanan harian penyebaran penyakit DBD
            </CardDescription>
          </CardHeader>

          <div className="grid grid-cols-2 gap-4 px-6">
            <div className="space-y-1">
              <Label>Masukkan jumlah kasus DBD</Label>
              <Input
                type="number"
                value={predictionData.kasus_dbd}
                onChange={(e) =>
                  setPredictionData({
                    ...predictionData,
                    kasus_dbd: Number(e.target.value),
                  })
                }
              />
            </div>
            <div className="space-y-1">
              <Label>Masukkan suhu rata-rata</Label>
              <Input
                type="number"
                value={predictionData.temp_avg}
                onChange={(e) =>
                  setPredictionData({
                    ...predictionData,
                    temp_avg: Number(e.target.value),
                  })
                }
              />
            </div>
            <div className="space-y-1">
              <Label>Masukkan kelembapan rata-rata</Label>
              <Input
                type="number"
                value={predictionData.humidity_avg}
                onChange={(e) =>
                  setPredictionData({
                    ...predictionData,
                    humidity_avg: Number(e.target.value),
                  })
                }
              />
            </div>
            <div className="space-y-1">
              <Label>Masukkan curah hujan</Label>
              <Input
                type="number"
                value={predictionData.rainfall_rate}
                onChange={(e) =>
                  setPredictionData({
                    ...predictionData,
                    rainfall_rate: Number(e.target.value),
                  })
                }
              />
            </div>
            <div className="space-y-1">
              <Label>Masukkan kepadatan penduduk</Label>
              <Input
                type="number"
                value={predictionData.kepadatan_penduduk}
                onChange={(e) =>
                  setPredictionData({
                    ...predictionData,
                    kepadatan_penduduk: Number(e.target.value),
                  })
                }
              />
            </div>
          </div>

          <CardFooter className="flex flex-col gap-4 p-6">
            <div className="flex items-center justify-end w-full">
              <Button
                disabled={predictionData.isLoading}
                onClick={onClickButtonPredict}
              >
                {predictionData.isLoading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Dices className="w-4 h-4 mr-2" />
                )}
                Prediksi
              </Button>
            </div>

            {predictionData.result && (
              <Alert>
              <AudioWaveform className="w-4 h-4" />
              <AlertTitle>Berhasil!</AlertTitle>
              <AlertDescription>
                Hasil prediksi tingkat kerentanan terhadap penyakit DBD terhadap beberapa parameter yang Anda masukkan adalah{" "}
                <Badge
                  className={cn(
                    predictionData.result === "High Risk DBD" && "font-medium text-sm bg-red-100 text-red-500 hover:bg-red-100",
                    predictionData.result === "Medium Risk DBD" && "font-medium text-sm bg-amber-100 text-amber-500 hover:bg-amber-100",
                    predictionData.result === "Low Risk DBD" && "font-medium text-sm bg-green-100 text-green-500 hover:bg-green-100"
                  )}
                >
                  {predictionData.result}
                </Badge>
              </AlertDescription>
            </Alert>
            )}
          </CardFooter>
        </Card>

        <Card className="mt-4">
          <CardHeader>
            <CardTitle className="text-lg">Plot</CardTitle>
            <CardDescription>
              Berikut plot data harian sebelum dan sesudah dilakukan clustering
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <Tabs defaultValue="before">
              <TabsList>
                <TabsTrigger value="before">Sebelum Clustering</TabsTrigger>
                <TabsTrigger value="after">Sesudah Clustering</TabsTrigger>
              </TabsList>
              <TabsContent value="before" className="mt-4">
                <img src={apiBaseUrl + "image/before-clustering"} />
              </TabsContent>
              <TabsContent value="after" className="mt-4">
                <img src={apiBaseUrl + "image/after-clustering"} />
              </TabsContent>
            </Tabs>
          </CardFooter>
        </Card>

        <Card className="mt-2">
          <CardHeader>
            <CardTitle className="text-lg">Data</CardTitle>
            <CardDescription>
              Berikut data harian setelah dilakukan clustering, maka data tersebut 
              akan digunakan untuk memprediksi tingkat kerentanan harian penyebaran penyakit DBD
            </CardDescription>
          </CardHeader>
          <CardFooter className="flex flex-col items-start gap-4">
            <Select
              defaultValue={filterData}
              onValueChange={(e) => setFilterData(e)}
            >
              <SelectTrigger className="w-72">
                <SelectValue placeholder="Filter data" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="-1">Semua</SelectItem>
                <SelectItem value="1">Low Risk</SelectItem>
                <SelectItem value="0">Medium Risk</SelectItem>
                <SelectItem value="2">High Risk</SelectItem>
              </SelectContent>
            </Select>

            <div className="w-full overflow-hidden border rounded-md">
              <Table>
                <TableHeader className="bg-muted/70">
                  <TableRow>
                    <TableHead>Tanggal</TableHead>
                    <TableHead>Kasus DBD</TableHead>
                    <TableHead>Kelembapan</TableHead>
                    <TableHead>Curah Hujan</TableHead>
                    <TableHead>Suhu</TableHead>
                    <TableHead>Kepadatan Penduduk</TableHead>
                    <TableHead>Cluster</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data
                    .filter((item) => {
                      const filter = Number(filterData);
                      if (filter === -1) return item;
                      else return item.cluster === filter;
                    })
                    .map((item, index) => (
                      <TableRow key={"data-item-" + index}>
                        <TableCell>
                          <FormattedDate
                            value={item.tanggal}
                            dateStyle="full"
                          />
                        </TableCell>
                        <TableCell>
                          <FormattedNumber value={item.kasus_dbd} />
                        </TableCell>
                        <TableCell>
                          <FormattedNumber value={item.humidity_avg} />
                        </TableCell>
                        <TableCell>
                          <FormattedNumber value={item.rainfall_rate} />
                        </TableCell>
                        <TableCell>
                          <FormattedNumber value={item.temp_avg} />
                        </TableCell>
                        <TableCell>
                          <FormattedNumber value={item.kepadatan_penduduk} />
                        </TableCell>
                        <TableCell>
                          <Badge
                            className={cn(
                              item.cluster === 2 &&
                                "text-sm bg-red-100 text-red-500 hover:bg-red-100",
                              item.cluster === 1 &&
                                "text-sm bg-green-100 text-green-500 hover:bg-green-100",
                              item.cluster === 0 &&
                                "text-sm bg-amber-100 text-amber-500 hover:bg-amber-100"
                            )}
                          >
                            {["Medium", "Low", "High"][item.cluster]}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </div>
          </CardFooter>
        </Card>
      </div>
    </>
  );
}
