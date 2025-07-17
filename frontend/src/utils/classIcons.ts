export type StageRow = { id: number; name: string }[];

export interface Branch {
  key: string;
  pt: string;
  stages: StageRow[]; // 6 linhas
}

export const iconUrl = (id: number, enabled: boolean) =>
  `https://static.divine-pride.net/images/jobs/${enabled ? "" : "disabled/"}icon_jobs_${id}.png`;

export const BRANCHES: Branch[] = [
  {
    key: "novice",
    pt: "Aprendizes",
    stages: [
      [{ id: 0, name: "Aprendiz" }],
      [{ id: 23, name: "Aprendiz Superior" }],
      [{ id: 4190, name: "Superaprendiz" }],
      [],
      [],
      [{ id: 4307, name: "Super Novice Ex" }],
    ],
  },
  {
    key: "acolyte",
    pt: "Sacerdotes",
    stages: [
      [{ id: 4, name: "Noviço" }],
      [{ id: 8, name: "Sacerdote" }, { id: 15, name: "Monge" }],
      [{ id: 4005, name: "Arquidiácono" }],
      [{ id: 4009, name: "Abade" }, { id: 4016, name: "Shura" }],
      [{ id: 4057, name: "Arcebispo" }, { id: 4070, name: "Shura EX" }],
      [{ id: 4256, name: "Cardeal" }, { id: 4262, name: "Shura Supremo" }],
    ],
  },
  {
    key: "archer",
    pt: "Arqueiros",
    stages: [
      [{ id: 3, name: "Arqueiro" }],
      [{ id: 11, name: "Caçador" }, { id: 19, name: "Bardo" }, { id: 20, name: "Odalisca" }],
      [{ id: 4004, name: "Sentinela" }],
      [{ id: 4012, name: "Guardião" }, { id: 4020, name: "Trovador" }, { id: 4021, name: "Musa" }],
      [{ id: 4056, name: "Sentinela Supremo" }, { id: 4068, name: "Troubadour" }, { id: 4069, name: "Trouvere" }],
      [{ id: 4257, name: "Atirador Divino" }, { id: 4263, name: "Maestro" }, { id: 4264, name: "Maestrina" }],
    ],
  },
  {
    key: "magician",
    pt: "Magos",
    stages: [
      [{ id: 2, name: "Mago" }],
      [{ id: 9, name: "Feiticeiro" }, { id: 16, name: "Sábio" }],
      [{ id: 4003, name: "Arcano" }],
      [{ id: 4010, name: "Arcano Supremo" }, { id: 4017, name: "Professor" }],
      [{ id: 4055, name: "Arcano Divino" }, { id: 4067, name: "Feiticeiro Supremo" }],
      [{ id: 4255, name: "Arcanista" }, { id: 4261, name: "Encantador Supremo" }],
    ],
  },
  {
    key: "merchant",
    pt: "Mercadores",
    stages: [
      [{ id: 5, name: "Mercador" }],
      [{ id: 10, name: "Ferreiro" }, { id: 18, name: "Alquimista" }],
      [{ id: 4006, name: "Mestre Ferreiro" }],
      [{ id: 4011, name: "Mecânico" }, { id: 4019, name: "Criador" }],
      [{ id: 4058, name: "Engenheiro" }, { id: 4071, name: "Bioquímico" }],
      [{ id: 4253, name: "Mestre Engenheiro" }, { id: 4259, name: "Geneticista" }],
    ],
  },
  {
    key: "swordman",
    pt: "Espadachins",
    stages: [
      [{ id: 1, name: "Espadachim" }],
      [{ id: 7, name: "Cavaleiro" }, { id: 14, name: "Templário" }],
      [{ id: 4002, name: "Lorde" }],
      [{ id: 4008, name: "Cavaleiro Rúnico" }, { id: 4015, name: "Guardião Real" }],
      [{ id: 4054, name: "Guardião Rúnico" }, { id: 4066, name: "Paladino Supremo" }],
      [{ id: 4252, name: "Senhor Supremo" }, { id: 4258, name: "Guardião Sagrado" }],
    ],
  },
  {
    key: "thief",
    pt: "Gatunos",
    stages: [
      [{ id: 6, name: "Gatuno" }],
      [{ id: 12, name: "Mercenário" }, { id: 17, name: "Renegado" }],
      [{ id: 4007, name: "Algoz" }],
      [{ id: 4013, name: "Sicário" }, { id: 4018, name: "Renegado" }],
      [{ id: 4059, name: "Executor" }, { id: 4072, name: "Infiltrador" }],
      [{ id: 4254, name: "Assassino Supremo" }, { id: 4260, name: "Mestre Renegado" }],
    ],
  },
  {
    key: "taekwon",
    pt: "Taekwons",
    stages: [
      [{ id: 4046, name: "Taekwon Kid" }],
      [{ id: 4047, name: "Taekwon Master" }],
      [{ id: 4239, name: "Star Gladiator" }],
      [],
      [{ id: 4302, name: "Sky Emperor" }],
      [],
    ],
  },
  {
    key: "espiritualista",
    pt: "Espiritualistas",
    stages: [
      [],
      [{ id: 4049, name: "Espiritualista" }],
      [],
      [{ id: 4240, name: "Soul Reaper" }],
      [{ id: 4303, name: "Soul Ascetic" }],
      [],
    ],
  },
  {
    key: "ninja",
    pt: "Ninjas",
    stages: [
      [{ id: 25, name: "Ninja" }],
      [{ id: 4211, name: "Kagerou" }, { id: 4212, name: "Oboro" }],
      [],
      [],
      [{ id: 4304, name: "Imperial Kagerou" }, { id: 4305, name: "Imperial Oboro" }],
      [],
    ],
  },
  {
    key: "gunslinger",
    pt: "Justiceiros",
    stages: [
      [{ id: 24, name: "Justiceiro" }],
      [{ id: 4215, name: "Rebellion" }],
      [],
      [],
      [],
      [{ id: 4306, name: "Peacemaker" }],
    ],
  },
  {
    key: "doram",
    pt: "Summoners",
    stages: [
      [{ id: 4218, name: "Doram" }],
      [],
      [],
      [],
      [],
      [{ id: 4308, name: "Doramic" }],
    ],
  },
];

export interface ItemLike {
  equipJobs?: (number | string)[];
  allowedClasses?: (number | string)[];
}

export function allowedIdSet(item: ItemLike): Set<number> {
  const arr = [
    ...(item.equipJobs ?? []),
    ...(item.allowedClasses ?? []),
  ];
  return new Set(
    arr
      .filter((v): v is number | string => v != null)
      .map((v) => (typeof v === "string" && /^\d+$/.test(v) ? Number(v) : v))
      .filter((v): v is number => typeof v === "number")
  );
}