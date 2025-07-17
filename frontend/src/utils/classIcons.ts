export type StageRow = number[];
export interface Branch {
  key: string;
  pt:  string;
  stages: StageRow[];
}

export const iconUrl = (id: number, enabled: boolean) =>
  `https://static.divine-pride.net/images/jobs/${enabled ? "" : "disabled/"}icon_jobs_${id}.png`;

export const BRANCHES: Branch[] = [
  { key: "novice", pt: "Aprendizes", stages: [[0], [23], [4190], [], [], [4307]] },
  { key: "acolyte", pt: "Sacerdotes", stages: [[4], [8, 15], [4005], [4009, 4016], [4057, 4070], [4256, 4262]] },
  { key: "archer", pt: "Arqueiros", stages: [[3], [11, 19, 20], [4004], [4012, 4020, 4021], [4056, 4068, 4069], [4257, 4263, 4264]] },
  { key: "magician", pt: "Magos", stages: [[2], [9, 16], [4003], [4010, 4017], [4055, 4067], [4255, 4261]] },
  { key: "merchant", pt: "Mercadores", stages: [[5], [10, 18], [4006], [4011, 4019], [4058, 4071], [4253, 4259]] },
  { key: "swordman", pt: "Espadachins", stages: [[1], [7, 14], [4002], [4008, 4015], [4054, 4066], [4252, 4258]] },
  { key: "thief", pt: "Gatunos", stages: [[6], [12, 17], [4007], [4013, 4018], [4059, 4072], [4254, 4260]] },
  { key: "taekwon", pt: "Taekwons", stages: [[4046], [4047], [4239], [], [4302], []] },
  { key: "espiritualista", pt: "Espiritualistas", stages: [[], [4049], [], [4240], [4303], []] },
  { key: "ninja", pt: "Ninjas", stages: [[25], [4211, 4212], [], [], [4304, 4305], []] },
  { key: "gunslinger", pt: "Justiceiros", stages: [[24], [4215], [], [], [], [4306]] },
  { key: "doram", pt: "Summoners", stages: [[4218], [], [], [], [], [4308]] },
];
